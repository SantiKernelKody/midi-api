from sqlalchemy import Column, Integer, String
from db.base_class import Base

class Stage(Base):
    __tablename__ = "stage"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(8))
    name = Column(String(32))
    description = Column(String(128))
