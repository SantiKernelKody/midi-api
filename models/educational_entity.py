from sqlalchemy import Column, Integer, String, TIMESTAMP
from db.base_class import Base

class EducationalEntity(Base):
    __tablename__ = "educational_entity"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    code = Column(String(16), nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
