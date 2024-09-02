from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

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
    class Config:
        orm_mode = True
        from_attributes = True

class LevelInDB(LevelInDBBase):
    pass




class LevelUpdate(BaseModel):
    name: str
    description: Optional[str]
    evaluation_criteria: Optional[str]
    max_score: int
    skill_ids: List[int]

    class Config:
        orm_mode = True
        
class LevelWithSkillsSchema(BaseModel):
    id: int
    name: str
    description: str
    evaluation_criteria: str
    max_score: int
    skill_ids: List[int]

    class Config:
        orm_mode = True