from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LevelBase(BaseModel):
    name: str
    description: Optional[str]
    evaluation_criteria: Optional[str]
    evaluation_method: Optional[str]
    max_score: Optional[int]

class LevelCreate(LevelBase):
    chapter_id: int

class LevelUpdate(LevelBase):
    chapter_id: Optional[int] = None

class LevelInDBBase(LevelBase):
    id: int
    chapter_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Level(LevelInDBBase):
    pass

class LevelInDB(LevelInDBBase):
    pass
