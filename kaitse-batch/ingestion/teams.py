from dotenv import load_dotenv
load_dotenv()

import os
import requests

import re
import uuid
from bs4 import BeautifulSoup

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
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

        teams[tm_team_id] = {"id": str(uuid.uuid4()), "name": name, "url": href}

    return [{"tm_team_id": k,  "id": v["id"], "name": v["name"], "url": v["url"]} for k, v in teams.items()]

def upsert_teams(teams: list[dict]) -> None:
    #sb = supabase_client()

    # TODO: valori cablati per la sola Serie A, in futuro va generalizzato
    payload = {"code": "IT1", "name": "Serie A Enilive", "country_code": "ITA", "level": 1, "organizer": "Italy"}
    api_base_url = os.getenv("KAITSE_API_BASE_URL", "http://localhost:8000").rstrip("/")

    resp = requests.post(
        f"{api_base_url}/api/v1/competitions/",
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()

    body = resp.json()
    comp = body.get("data", body) if isinstance(body, dict) else {}
    competition_code = comp.get("code", payload["code"])

    logger.info(f"competition synced via API: code={competition_code}")

    for t in teams:
        team_payload = {
            "tm_team_id": t["tm_team_id"],
            "name": t["name"],
            "city": "",
            "image_path": "",
        }

        resp = requests.post(
            f"{api_base_url}/api/v1/teams/",
            json=team_payload,
            timeout=30,
        )
        resp.raise_for_status()

    logger.info(f"teams synced via API: count={len(teams)}")

    # upsert relazione competizione - stagione
    """
    existing = sb.table("competition_seasons").select("competition_id, season_code").eq("competition_id", competition_code).execute().data
    existing_season_code= {e["season_code"] for e in existing}

    #TODO: valore cablato per la stagione 2025-2026, in futuro va generalizzato per altre stagioni
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
"""

