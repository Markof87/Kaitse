from dotenv import load_dotenv
load_dotenv()

import re
from bs4 import BeautifulSoup
from ingestion.config import supabase_client
from utils.logging_config import setup_logging

logger = setup_logging(__name__)

TEAM_ID_RE = re.compile(r"/verein/(\d+)")

def parse_teams(html: str):
    soup = BeautifulSoup(html, "lxml")

    teams = {}
    for a in soup.select("a[href*='/verein/']"):
        href = a.get("href") or ""
        m = TEAM_ID_RE.search(href)
        if not m:
            continue
        tm_team_id = int(m.group(1))
        name = a.get_text(strip=True)
        if not name:
            continue

        teams[tm_team_id] = name

    return [{"tm_team_id": k, "name": v} for k, v in teams.items()]

def upsert_teams(teams: list[dict]) -> None:
    sb = supabase_client()

    comp = sb.table("competitions").upsert(
        #TODO: valori cablati per la sola serie A, in futuro va generalizzato per altre competizioni
        {"code": "IT1", "name": "Serie A", "country_code": "ITA"},
        on_conflict="code"
    ).execute().data[0]

    competition_code = comp["code"]
    logger.info(f"competition upserted: code={competition_code} code=IT1")

    sb.table("teams").upsert(
        [{"tm_team_id": t["tm_team_id"], "name": t["name"]} for t in teams],
        on_conflict="tm_team_id"
    ).execute()

    logger.info(f"teams upserted: count={len(teams)}")

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
    for t in teams: 
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


