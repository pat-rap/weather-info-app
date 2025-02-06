# src/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

Base = declarative_base()

class FeedMeta(Base):
    __tablename__ = "feed_meta"

    id = Column(Integer, primary_key=True, index=True)
    feed_url = Column(String, nullable=False)
    feed_title = Column(String)
    feed_subtitle = Column(String)
    feed_updated = Column(DateTime(timezone=True))
    feed_id_in_atom = Column(String)
    rights = Column(String)
    category = Column(String)
    frequency_type = Column(String)
    last_fetched = Column(DateTime(timezone=True))

    entries = relationship("FeedEntry", back_populates="feed_meta")

class FeedEntry(Base):
    __tablename__ = "feed_entries"

    id = Column(Integer, primary_key=True, index=True)
    feed_id = Column(Integer, ForeignKey("feed_meta.id"), nullable=False)
    entry_id_in_atom = Column(String, nullable=False, unique=True)
    entry_title = Column(String)
    entry_updated = Column(DateTime(timezone=True))
    entry_author = Column(String)
    entry_link = Column(String)
    entry_content = Column(Text)
    inserted_at = Column(DateTime(timezone=True))

    feed_meta = relationship("FeedMeta", back_populates="entries")
