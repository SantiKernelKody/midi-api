from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from db.base_class import Base
from datetime import datetime
from sqlalchemy.orm import relationship
class PlayerStory(Base):
    __tablename__ = "player_story"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    stage_id = Column(Integer, ForeignKey("stage.id"))
    story_id = Column(Integer, ForeignKey("story.id"))
    player_id = Column(Integer, ForeignKey("player.id"))
    time_watched = Column(Integer)
    total_time_out = Column(Integer)
    pauses = Column(Integer)
    times_out_focus = Column(Integer)
    state = Column(String(64))
    created_at = Column(DateTime, default=datetime.utcnow)

    stage = relationship("Stage", back_populates="player_stories")
    story = relationship("Story", back_populates="player_stories")
    player = relationship("Player", back_populates="player_stories")