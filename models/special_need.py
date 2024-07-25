from sqlalchemy import Column, Integer, String
from db.base_class import Base

class SpecialNeed(Base):
    __tablename__ = "special_need"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(128), index=True)
    description = Column(String(500))
