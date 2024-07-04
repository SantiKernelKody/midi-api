from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db.base_class import Base

class Chapter(Base):
    __tablename__ = "chapter"
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    name = Column(String(64))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
