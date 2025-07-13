# scraper/telegram_scraper.py

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
from telethon.utils import get_display_name
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import os
import json

# Load environment variables
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")

client = TelegramClient("medical_scraper", api_id, api_hash)

def scrape_channel_messages(channel_username, limit=100):
    client.start()
    channel = client.get_entity(channel_username)
    messages = []

    # Set up save paths
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    json_path = Path(f"data/raw/telegram_messages/{date_str}")
    img_path = Path(f"data/raw/images/{channel_username.replace('@','')}")
    json_path.mkdir(parents=True, exist_ok=True)
    img_path.mkdir(parents=True, exist_ok=True)

    # Fetch messages
    history = client(GetHistoryRequest(
        peer=channel,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))

    for message in history.messages:
        entry = {
            "id": message.id,
            "date": message.date.strftime('%Y-%m-%d %H:%M:%S'),
            "text": message.message or "",
            "has_media": bool(message.media),
            "channel": channel_username
        }

        # Download media if present
        if message.media and isinstance(message.media, (MessageMediaPhoto, MessageMediaDocument)):
            try:
                img_file = img_path / f"{message.id}.jpg"
                client.download_media(message.media, file=img_file)
                entry["image_path"] = str(img_file)
            except Exception as e:
                entry["media_error"] = str(e)

        messages.append(entry)

    # Save messages to JSON
    output_file = json_path / f"{channel_username.replace('@', '')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    print(f"✅ Saved {len(messages)} messages (with images if available) to {output_file}")
    client.disconnect()

if __name__ == "__main__":
    medical_channels = [
        "@CheMed123",
        "@lobelia4cosmetics",
        "@tikvahpharma"
        # Add more from https://et.tgstat.com/medicine
    ]

    for ch in medical_channels:
        try:
            scrape_channel_messages(ch, limit=200)
        except Exception as e:
            print(f"❌ Error scraping {ch}: {e}")

