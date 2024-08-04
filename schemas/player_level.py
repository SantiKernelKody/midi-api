from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlayerLevelBase(BaseModel):
    score: float
    incorrect: int
    correct: int
    attempts: int
    total_time: int
    times_out_focus: int
    state: Optional[str] = None

class PlayerLevelCreate(PlayerLevelBase):
    level_id: int
    player_id: int

class PlayerLevelUpdate(PlayerLevelBase):
    level_id: Optional[int] = None
    player_id: Optional[int] = None

class PlayerLevelInDBBase(PlayerLevelBase):
    id: int
    level_id: int
    player_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PlayerLevel(PlayerLevelInDBBase):
    pass

class PlayerLevelInDB(PlayerLevelInDBBase):
    pass
