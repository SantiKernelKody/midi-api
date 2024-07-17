from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.base_class import Base

class EducationReviewer(Base):
    __tablename__ = "education_reviewer"

    id = Column(Integer, primary_key=True, index=True)
    education_id = Column(Integer, ForeignKey("educational_entity.id"))
    reviewer_id = Column(Integer, ForeignKey("dashboard_user.id"))

    education = relationship("EducationalEntity")
    reviewer = relationship("DashboardUser")
