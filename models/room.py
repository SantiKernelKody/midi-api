from sqlalchemy import Column, Integer, DateTime, ForeignKey
from db.base_class import Base
from datetime import datetime

class Room(Base):
    __tablename__ = "room"
    id = Column(Integer, primary_key=True, index=True)
    id_avatar = Column(Integer, ForeignKey("avatar.id"))
    id_stage = Column(Integer, ForeignKey("stage.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
