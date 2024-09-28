from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, MetaData, String
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base()


class Word(Base):
    __tablename__ = "words"
    metadata
    id = Column(Integer, primary_key=True)
    word = Column(String(75), nullable=False)
    translation = Column(String(75), nullable=False)
    tg_user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
