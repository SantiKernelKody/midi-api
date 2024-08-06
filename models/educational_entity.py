from sqlalchemy import Column, Integer, String, TIMESTAMP
from db.base_class import Base
from sqlalchemy.orm import relationship

class EducationalEntity(Base):
    __tablename__ = "educational_entity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    code = Column(String(16), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)

    players = relationship("Player", back_populates="school")
    courses = relationship("Course", back_populates="school")