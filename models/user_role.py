from sqlalchemy import Column, Integer, String
from db.base_class import Base

class UserRole(Base):
    __tablename__ = "user_role"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(32), index=True)
    display_name = Column(String(32))
    description = Column(String(255))
