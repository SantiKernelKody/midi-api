from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.base_class import Base
from sqlalchemy.orm import relationship

class Game(Base):
    __tablename__ = "game"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(64))
    description = Column(String(255))
    logo_game = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    chapters = relationship("Chapter", back_populates="game")