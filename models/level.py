from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from db.base_class import Base

class Level(Base):
    __tablename__ = "level"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    chapter_id = Column(Integer, ForeignKey("chapter.id"))
    name = Column(String(64))
    description = Column(String(255))
    evaluation_criteria = Column(Text)
    evaluation_method = Column(Text)
    max_score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
