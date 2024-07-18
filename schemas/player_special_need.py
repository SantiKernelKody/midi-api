from pydantic import BaseModel

class PlayerSpecialNeedBase(BaseModel):
    player_id: int
    special_need_id: int

class PlayerSpecialNeedCreate(PlayerSpecialNeedBase):
    pass

class PlayerSpecialNeedUpdate(PlayerSpecialNeedBase):
    pass

class PlayerSpecialNeedInDBBase(PlayerSpecialNeedBase):
    id: int

    class Config:
        orm_mode = True

class PlayerSpecialNeed(PlayerSpecialNeedInDBBase):
    pass
