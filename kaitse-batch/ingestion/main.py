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

        upsert_teams(teams)

        for t in sorted(teams, key=lambda x: x["name"].lower()):
            logger.info(f"{t['tm_team_id']} - {t['name']}")
            print(t["tm_team_id"], "-", t["name"])

            html_players = fetch_html(TRANSFERMARKT_BASE_URL + t["url"].replace('spielplan', 'kader'))
            players = parse_players(html_players)
            logger.info(f"Extracted {len(players)} players for team {t['name']}")
            print(f"Players found for {t['name']}: {len(players)}")
            for p in sorted(players, key=lambda x: x["full_name"].lower()):
                logger.info(f"  {p['id']} - {p['full_name']} ({p['short_name']})")
                print(f"  {p['id']} - {p['full_name']} ({p['short_name']})")
                upsert_players([p])

    except Exception as e:
        logger.exception("Fatal error during ingestion")
        raise


    logger.info("Batch completed successfully")