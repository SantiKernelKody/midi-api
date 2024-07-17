from sqlalchemy import Column, Integer, String
from db.base_class import Base

class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
