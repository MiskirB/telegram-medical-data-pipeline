from fastapi import FastAPI, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
from typing import List

app = FastAPI(title="Telegram Medical Analytics API")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Top Products Endpoint
@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def top_products(
    limit: int = Query(10, ge=1, le=100, description="Number of top products to return"),
    db: Session = Depends(get_db)
):
    rows = crud.get_top_products(db, limit)
    if not rows:
        raise HTTPException(status_code=404, detail="No top products found.")
    return [{"product_name": r[0], "mentions": r[1]} for r in rows]

# ✅ Channel Activity Endpoint
@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def channel_activity(
    channel_name: str = Path(..., description="Name of the channel"),
    db: Session = Depends(get_db)
):
    rows = crud.get_channel_activity(db, channel_name)
    if not rows:
        raise HTTPException(status_code=404, detail=f"No activity found for channel '{channel_name}'.")
    return [{"message_date": r[0], "message_count": r[1]} for r in rows]

# ✅ Keyword Search Endpoint
@app.get("/api/search/messages", response_model=List[schemas.Message])
def search(
    keyword: str = Query(..., min_length=2, description="Keyword to search in messages"),
    db: Session = Depends(get_db)
):
    rows = crud.search_messages(db, keyword)
    if not rows:
        raise HTTPException(status_code=404, detail=f"No messages found containing '{keyword}'.")
    return [dict(r._mapping) for r in rows]
