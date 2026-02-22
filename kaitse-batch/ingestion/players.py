from dotenv import load_dotenv
load_dotenv()

import re
from bs4 import BeautifulSoup
from ingestion.config import supabase_client
from utils.logging_config import setup_logging

logger = setup_logging(__name__)

PLAYER_ID_RE = re.compile(r"/spieler/(\d+)")

def parse_players(html: str):
    soup = BeautifulSoup(html, "lxml")

    players = {}
    for a in soup.select("a[href*='/spieler/']"):
        print(a)
        href = a.get("href") or ""
        m = PLAYER_ID_RE.search(href)
        if not m:
            continue
        player_id = int(m.group(1))
        name = a.get_text(strip=True)
        if not name:
            continue

        players[player_id] = name

    return [{"player_id": k, "name": v} for k, v in players.items()]

def upsert_players(players: list[dict]) -> None:
    sb = supabase_client()

    comp = sb.table("competitions").upsert(
        #TODO: valori cablati per la sola serie A, in futuro va generalizzato per altre competizioni
        {"code": "IT1", "name": "Serie A", "country_code": "ITA"},
        on_conflict="code"
    ).execute().data[0]

    competition_code = comp["code"]
    logger.info(f"competition upserted: code={competition_code} code=IT1")

    sb.table("players").upsert(
        [{"tm_team_id": t["tm_team_id"], "name": t["name"]} for t in players],
        on_conflict="tm_team_id"
    ).execute()

    logger.info(f"players upserted: count={len(players)}")

    # upsert relazione competizione - stagione
    existing = sb.table("competition_seasons").select("competition_id, season_code").eq("competition_id", competition_code).execute().data
    existing_season_code= {e["season_code"] for e in existing}
    season_code = "2025-2026"
    if season_code not in existing_season_code:
        sb.table("competition_seasons").insert({"competition_id": competition_code, "season_code": season_code}).execute()
        logger.info(f"competition_seasons relation inserted: season_code={season_code}")
    else:
        logger.info(f"competition_seasons relation already exists: season_code={season_code}")

    existing = sb.table("competition_season_teams").select("competition_id, season_code, team_id").eq("competition_id", competition_code).execute().data
    existing_team_ids = {e["team_id"] for e in existing}
    team_ids_to_add = []
    for t in players: 
        team = sb.table("teams").select("tm_team_id").eq("tm_team_id", t["tm_team_id"]).execute().data[0]
        team_id = team["tm_team_id"]
        if team_id not in existing_team_ids:
            team_ids_to_add.append(team_id)

    if team_ids_to_add:
        sb.table("competition_season_teams").insert(
            [{"competition_id": competition_code, "season_code": season_code, "team_id": tid} for tid in team_ids_to_add]
        ).execute()
        logger.info(f"competition_season_teams relations inserted: count={len(team_ids_to_add)}")
    else:
        logger.info("No new competition_season_teams relations to insert")


