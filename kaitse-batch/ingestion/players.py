from dotenv import load_dotenv
load_dotenv()

import re
from bs4 import BeautifulSoup
from ingestion.config import fetch_html, supabase_client
from utils.logging_config import setup_logging
import uuid

logger = setup_logging(__name__)

PLAYER_ID_RE = re.compile(r"/spieler/(\d+)")
TRANSFERMARKT_BASE_URL = "https://www.transfermarkt.it"

def parse_players(html: str):
    soup = BeautifulSoup(html, "lxml")
    
    players = {}
    for a in soup.select("a[href*='/profil/spieler/']"):
        href = a.get("href") or ""
        m = PLAYER_ID_RE.search(href)
        if not m:
            continue

        player_id = int(m.group(1))
        name = a.get_text(strip=True)
        if not name:
            continue

        short_name = name.split()[-1] if name else ""
        transfermarkt_id = player_id

        player_info = get_player_transfermarkt_info(TRANSFERMARKT_BASE_URL + href)
        
        # Clean special characters from names
        cleaned_name = re.sub(r'[^\w\s-]', '', name, flags=re.UNICODE)
        cleaned_name = ''.join(c for c in cleaned_name if ord(c) < 128 or c.isspace() or c == '-').replace(" ", "-").lower()
        
        players[player_id] = {
            "full_name": name,
            "slug": cleaned_name,
            "image_path": f'players/{cleaned_name}.jpg',
            "short_name": short_name,
            "transfermarkt_id": transfermarkt_id,
            **player_info
        }

    return [{"id": k, "full_name": v["full_name"], "short_name": v["short_name"], "transfermarkt_id": v["transfermarkt_id"], **v} for k, v in players.items()]

def get_player_transfermarkt_info(url: str) -> dict:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "lxml")

    player_info = {
        'birth_date': None,
        'height': None,
        'weight': None,
        'preferred_foot': None,
    }
    
    # Find the info-table elements that contain player data
    info_tables = soup.find_all('div', class_='info-table info-table--right-space')
    
    if info_tables:
        info_table = info_tables[0]
        
        # Find all label-content pairs
        labels = info_table.find_all('span', class_='info-table__content info-table__content--regular')
        contents = info_table.find_all('span', class_='info-table__content info-table__content--bold')
        
        # Map labels to their corresponding content
        for i, label in enumerate(labels):
            label_text = label.get_text(strip=True).lower()
            
            if i < len(contents):
                content_text = contents[i].get_text(strip=True)
                
                if 'nato il' in label_text or 'data di nascita' in label_text:
                    player_info['birth_date'] = re.sub(r'\s*\(.*\)|\s*Buon compleanno', '', content_text).strip()
                    if player_info['birth_date']:
                        player_info['birth_date'] = '-'.join(reversed(player_info['birth_date'].split('/')))
                elif 'altezza' in label_text:
                    height_str = content_text.replace('\xa0', '').replace(',', '.')
                    try:
                        height_m = float(re.sub(r'\s*m$', '', height_str))
                        player_info['height'] = int(height_m * 100)
                    except ValueError:
                        player_info['height'] = None

                elif 'peso' in label_text:
                    player_info['weight'] = content_text
                elif 'piede' in label_text:
                    foot = content_text.lower()
                    if 'destro' in foot:
                        player_info['preferred_foot'] = 'Right'
                    elif 'entrambi' in foot:
                        player_info['preferred_foot'] = 'Both'
                    else:
                        player_info['preferred_foot'] = 'Left'
    
    return player_info

def upsert_players(players: list[dict]) -> None:
    sb = supabase_client()

    sb.table("players").upsert(
        [{
            "id": str(uuid.uuid4()),
            "full_name": p["full_name"],
            "short_name": p["short_name"],
            "slug": p["slug"],
            "image_path": p["image_path"],
            "transfermarkt_id": p["transfermarkt_id"],
            "birth_date": p.get("birth_date"),
            "height": p.get("height"),
            "weight": p.get("weight"),
            "preferred_foot": p.get("preferred_foot"),
        } for p in players]
    ).execute()

    logger.info(f"players upserted: count={len(players)}")




