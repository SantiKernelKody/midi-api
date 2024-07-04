from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db.base_class import Base

class Story(Base):
    __tablename__ = "story"
    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    time = Column(Integer)
    name = Column(String(64))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
