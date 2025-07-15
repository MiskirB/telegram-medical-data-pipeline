from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Message(BaseModel):
    id: int
    message_date: date
    text: str
    has_media: bool
    channel_name: str
    message_day: date
    month_name: str
    year: int
    message_length: int

class ChannelActivity(BaseModel):
    message_date: date
    message_count: int

class TopProduct(BaseModel):
    product_name: str
    mentions: int
