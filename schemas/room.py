from pydantic import BaseModel
from datetime import datetime

class RoomBase(BaseModel):
    id_avatar: int
    id_stage: int
    player_id: int

class RoomCreate(RoomBase):
    pass

class RoomUpdate(RoomBase):
    pass

class RoomInDBBase(RoomBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class Room(RoomInDBBase):
    pass

class RoomInDB(RoomInDBBase):
    pass
