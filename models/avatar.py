from sqlalchemy import Column, Integer, String
from db.base_class import Base

class Avatar(Base):
    __tablename__ = "avatar"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32))
    description = Column(String(64))
