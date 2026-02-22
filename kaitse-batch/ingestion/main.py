from utils.logging_config import setup_logging
from ingestion.config import fetch_html
from ingestion.teams import parse_teams, upsert_teams

logger = setup_logging(__name__)

if __name__ == "__main__":
    URL = "https://www.transfermarkt.it/serie-a/startseite/wettbewerb/IT1"

    logger.info("Starting Teams ingestion")

    try:
        html = fetch_html(URL)
        teams = parse_teams(html)

        logger.info(f"Extracted {len(teams)} teams")
        print(f"Teams found: {len(teams)}")
        for t in sorted(teams, key=lambda x: x["name"].lower()):
            logger.info(f"{t['tm_team_id']} - {t['name']}")
            print(t["tm_team_id"], "-", t["name"])

    except Exception as e:
        logger.exception("Fatal error during ingestion")
        raise

    upsert_teams(teams)

    logger.info("Batch completed successfully")