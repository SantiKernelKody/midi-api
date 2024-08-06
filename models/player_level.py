from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from db.base_class import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class PlayerLevel(Base):
    __tablename__ = "player_level"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey("stage.id"))
    level_id = Column(Integer, ForeignKey("level.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    score = Column(Float(10, 2))
    incorrect = Column(Integer)
    correct = Column(Integer)
    attempts = Column(Integer)
    total_time = Column(Integer)
    times_out_focus = Column(Integer)
    state = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)

    stage = relationship("Stage", back_populates="player_levels")
    level = relationship("Level", back_populates="player_levels")
    player = relationship("Player", back_populates="player_levels")