from sqlalchemy import Column, Integer, String
from db.base_class import Base

class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
