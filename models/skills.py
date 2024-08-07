from sqlalchemy import Column, Integer, String
from db.base_class import Base

class Skills(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32))
    description = Column(String(255))
