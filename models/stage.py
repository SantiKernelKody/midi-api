from sqlalchemy import Column, Integer, String
from db.base_class import Base
from sqlalchemy.orm import relationship

class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(8))
    name = Column(String(32))
    description = Column(String(128))

    player_levels = relationship("PlayerLevel", back_populates="stage")
    player_stories = relationship("PlayerStory", back_populates="stage")