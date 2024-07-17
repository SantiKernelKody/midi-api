from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LevelBase(BaseModel):
    name: str
    description: str
    evaluation_criteria: str
    evaluation_method: str
    max_score: int

class LevelCreate(LevelBase):
    chapter_id: int

class LevelUpdate(LevelBase):
    chapter_id: Optional[int] = None

class LevelInDBBase(LevelBase):
    id: int
    chapter_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class Level(LevelInDBBase):
    pass

class LevelInDB(LevelInDBBase):
    pass
