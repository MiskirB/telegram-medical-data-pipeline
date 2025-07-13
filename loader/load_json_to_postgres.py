import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

# Load DB credentials
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def create_table_if_not_exists(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw_telegram_messages (
            id INTEGER PRIMARY KEY,
            message_date TIMESTAMP,
            text TEXT,
            has_media BOOLEAN,
            channel TEXT,
            image_path TEXT
        )
    """)

def load_json_files(data_dir):
    for file in Path(data_dir).rglob("*.json"):
        print(f"📥 Loading {file}")
        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)

        with connect_db() as conn:
            with conn.cursor() as cursor:
                create_table_if_not_exists(cursor)
                for msg in messages:
                    cursor.execute("""
                        INSERT INTO raw_telegram_messages (id, message_date, text, has_media, channel, image_path)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                    """, (
                        msg.get("id"),
                        msg.get("date"),
                        msg.get("text"),
                        msg.get("has_media"),
                        msg.get("channel"),
                        msg.get("image_path", None)
                    ))
            conn.commit()
        print(f"✅ Inserted {len(messages)} messages from {file.name}")

if __name__ == "__main__":
    data_path = "data/raw/telegram_messages"
    load_json_files(data_path)
