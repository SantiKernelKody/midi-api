from sqlalchemy import Column, Integer, String
from db.base_class import Base

class PoliticDivision(Base):
    __tablename__ = "politic_division"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
