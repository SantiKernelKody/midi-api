from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from db.base_class import Base
from datetime import datetime

class PlayerLevel(Base):
    __tablename__ = "player_level"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    level_id = Column(Integer, ForeignKey("level.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    score = Column(Float(10, 2))
    incorrect = Column(Integer)
    correct = Column(Integer)
    attempts = Column(Integer)
    total_time = Column(Integer)
    times_out_focus = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
