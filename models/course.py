from sqlalchemy import Column, Integer, String, ForeignKey
from db.base_class import Base

class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer)
    reviewer_id = Column(Integer)
    subject_name = Column(String(128))
    description = Column(String(255))
