from pydantic import BaseModel

class StageBase(BaseModel):
    code: str
    name: str
    description: str

class StageCreate(StageBase):
    pass

class StageUpdate(StageBase):
    pass

class StageInDBBase(StageBase):
    id: int

    class Config:
         from_attributes = True

class Stage(StageInDBBase):
    pass

class StageInDB(StageInDBBase):
    pass
