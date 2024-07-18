from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class CaretakerPlayer(Base):
    __tablename__ = "caretaker_player"

    id = Column(Integer, primary_key=True, index=True)
    representative_id = Column(Integer, ForeignKey("dashboard_user.id"))
    player_id = Column(Integer, ForeignKey("player.id"))

    representative = relationship("DashboardUser")
    player = relationship("Player")
