from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChapterBase(BaseModel):
    name: str
    description: str

class ChapterCreate(ChapterBase):
    game_id: int

class ChapterUpdate(ChapterBase):
    game_id: Optional[int] = None

class ChapterInDBBase(ChapterBase):
    id: int
    game_id: int
    created_at: datetime

    class Config:
         from_attributes = True

class Chapter(ChapterInDBBase):
    pass

class ChapterInDB(ChapterInDBBase):
    pass