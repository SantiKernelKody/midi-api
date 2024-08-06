from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship
from db.base_class import Base

class Player(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey("educational_entity.id"))
    special_need_id = Column(Integer, nullable=True)
    full_name = Column(String(128), nullable=False)
    edad = Column(Integer, nullable=True)
    ethnicity = Column(String(32), nullable=True)
    special_need_description = Column(String(255), nullable=True)
    special_need = Column(Boolean, nullable=True)
    user_name = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    school = relationship("EducationalEntity", back_populates="player")
    player_levels = relationship("PlayerLevel", back_populates="player")
    player_stories = relationship("PlayerStory", back_populates="player")
    #special_need = relationship("SpecialNeed")
