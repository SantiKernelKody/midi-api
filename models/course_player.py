from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class CoursePlayer(Base):
    __tablename__ = "course_player"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("course.id"))
    player_id = Column(Integer, ForeignKey("player.id"))

    course = relationship("Course", back_populates="players")
    player = relationship("Player", back_populates="courses")
