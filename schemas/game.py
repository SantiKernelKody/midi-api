from pydantic import BaseModel
from datetime import datetime
from typing import Optional
class GameBase(BaseModel):
    name: str
    description: str
    logo_game: Optional[str]

class GameCreate(GameBase):
    pass

class GameUpdate(GameBase):
    pass

class GameInDBBase(GameBase):
    id: int

    class Config:
        orm_mode = True

class Game(GameInDBBase):
    pass
