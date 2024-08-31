from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, MetaData, String
from sqlalchemy.orm import declarative_base, relationship

metadata = MetaData()

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    metadata
    id = Column(Integer, primary_key=True)
    chat_id_in_tg = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_superuser = Column(Boolean, default=False)

    words = relationship("Word", back_populates="user")


class Word(Base):
    __tablename__ = "words"
    metadata
    id = Column(Integer, primary_key=True)
    word = Column(String(50), nullable=False)
    translation = Column(String(50), nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"), nullable=False)  # ForeignKey на таблицу users

    # Связь с таблицей User
    user = relationship("User", back_populates="words")


# first_name = Column(String(40))
# last_name = Column(String(40))
# email = Column(String(60), unique=True, nullable=False, index=True)
# city = Column(String(70))
# phone = Column(String(30))
# avatar = Column(String(255))
# hashed_password = Column(String, nullable=False)
# is_superuser = Column(Boolean, default=False)
# is_active = Column(Boolean, default=True)
# created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
# updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda:
#
# datetime.now(timezone.utc))
