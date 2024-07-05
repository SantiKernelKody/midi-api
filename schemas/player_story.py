from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlayerStoryBase(BaseModel):
    time_watched: int
    total_time_out: int
    pauses: int
    times_out_focus: int

class PlayerStoryCreate(PlayerStoryBase):
    story_id: int
    player_id: int

class PlayerStoryUpdate(PlayerStoryBase):
    story_id: Optional[int] = None
    player_id: Optional[int] = None

class PlayerStoryInDBBase(PlayerStoryBase):
    id: int
    story_id: int
    player_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PlayerStory(PlayerStoryInDBBase):
    pass

class PlayerStoryInDB(PlayerStoryInDBBase):
    pass
