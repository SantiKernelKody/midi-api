from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    school_id = Column(Integer, ForeignKey("educational_entity.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("dashboard_user.id"), nullable=False)
    subject_name = Column(String(128), nullable=False)
    description = Column(String(255), nullable=True)

    school = relationship("EducationalEntity", back_populates="courses")
    reviewer = relationship("DashboardUser", back_populates="courses")
    players = relationship("CoursePlayer", back_populates="course")
