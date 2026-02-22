from utils.logging_config import setup_logging
from ingestion.config import fetch_html
from ingestion.teams import parse_teams, upsert_teams
from ingestion.players import parse_players, upsert_players

logger = setup_logging(__name__)

if __name__ == "__main__":
    TRANSFERMARKT_BASE_URL = "https://www.transfermarkt.it"
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

            html_player = fetch_html(TRANSFERMARKT_BASE_URL + t["url"])
            print(html_player)
            players = parse_players(html_player)
            print (players)

    except Exception as e:
        logger.exception("Fatal error during ingestion")
        raise

    #upsert_teams(teams)

    logger.info("Batch completed successfully")