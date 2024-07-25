from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class PlayerSpecialNeed(Base):
    __tablename__ = "player_special_need"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("player.id"))
    special_need_id = Column(Integer, ForeignKey("special_need.id"))

    player = relationship("Player")
    special_need = relationship("SpecialNeed")
