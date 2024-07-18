from pydantic import BaseModel

class CaretakerPlayerBase(BaseModel):
    representative_id: int
    player_id: int

class CaretakerPlayerCreate(CaretakerPlayerBase):
    pass

class CaretakerPlayerUpdate(CaretakerPlayerBase):
    pass

class CaretakerPlayerInDBBase(CaretakerPlayerBase):
    id: int

    class Config:
        orm_mode = True

class CaretakerPlayer(CaretakerPlayerInDBBase):
    pass
