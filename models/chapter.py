from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db.base_class import Base
from sqlalchemy.orm import relationship

class Chapter(Base):
    __tablename__ = "chapter"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey("game.id"))
    name = Column(String(64))
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    game = relationship("Game", back_populates="chapters")
    levels = relationship("Level", back_populates="chapter")
    stories = relationship("Story", back_populates="chapter")