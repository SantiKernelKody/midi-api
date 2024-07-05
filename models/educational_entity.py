from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from db.base_class import Base

class EducationalEntity(Base):
    __tablename__ = "educational_entity"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    code = Column(String(16), unique=True, index=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
