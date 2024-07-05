from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StoryBase(BaseModel):
    time: int
    name: str
    description: str

class StoryCreate(StoryBase):
    chapter_id: int

class StoryUpdate(StoryBase):
    chapter_id: Optional[int] = None

class StoryInDBBase(StoryBase):
    id: int
    chapter_id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Story(StoryInDBBase):
    pass

class StoryInDB(StoryInDBBase):
    pass
