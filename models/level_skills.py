from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class LevelSkills(Base):
    __tablename__ = "level_skills"

    id = Column(Integer, primary_key=True, index=True)
    level_id = Column(Integer, ForeignKey("level.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))

    level = relationship("Level")
    skill = relationship("Skills")
