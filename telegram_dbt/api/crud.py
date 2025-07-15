from sqlalchemy.orm import Session
from sqlalchemy import text

def get_top_products(db: Session, limit: int = 10):
    query = text("""
        SELECT LOWER(SPLIT_PART(text, ' ', 1)) as product_name, COUNT(*) as mentions
        FROM fct_messages
        WHERE text IS NOT NULL
        GROUP BY product_name
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    return db.execute(query, {"limit": limit}).fetchall()

def get_channel_activity(db: Session, channel_name: str):
    query = text("""
        SELECT message_date::date, COUNT(*) AS message_count
        FROM fct_messages
        WHERE channel_name = :channel
        GROUP BY message_date::date
        ORDER BY message_date
    """)
    return db.execute(query, {"channel": channel_name}).fetchall()

def search_messages(db: Session, keyword: str):
    query = text("""
        SELECT 
            id,
            message_date,
            text,
            has_media,
            channel_name,
            message_day,
            month_name,
            year,
            message_length
        FROM fct_messages
        WHERE LOWER(text) LIKE :kw
        ORDER BY message_date DESC
        LIMIT 50
    """)
    return db.execute(query, {"kw": f"%{keyword.lower()}%"}).fetchall()

