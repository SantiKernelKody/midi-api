from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db.base_class import Base

class DashboardUser(Base):
    __tablename__ = "dashboard_user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("user_role.id"))
    name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(128), unique=False, index=True)
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    role = relationship("UserRole", back_populates="users")
    courses = relationship("Course", back_populates="reviewer")
