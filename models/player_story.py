from sqlalchemy import Column, Integer, DateTime, ForeignKey
from db.base_class import Base
from datetime import datetime
class PlayerStory(Base):
    __tablename__ = "player_story"
    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("story.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    time_watched = Column(Integer)
    total_time_out = Column(Integer)
    pauses = Column(Integer)
    times_out_focus = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
