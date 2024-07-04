from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from db.base_class import Base
from datetime import datetime

class Player(Base):
    __tablename__ = "player"
    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer)
    avatar_id = Column(Integer)
    special_need_id = Column(Integer)
    name = Column(String(128))
    last_name = Column(String(128))
    edad = Column(Integer)
    ethnicity = Column(String(32))
    special_need_description = Column(String(255))
    special_need = Column(Boolean)
    user_name = Column(String(255))
    password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
