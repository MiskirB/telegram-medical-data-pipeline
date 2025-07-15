# app/models.py
from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FctMessage(Base):
    __tablename__ = 'fct_messages'
    id = Column(Integer, primary_key=True, index=True)
    message_date = Column(Date)
    text = Column(Text)
    has_media = Column(Boolean)
    channel_name = Column(String)
    message_length = Column(Integer)

class DimChannel(Base):
    __tablename__ = 'dim_channels'
    channel_name = Column(String, primary_key=True, index=True)
