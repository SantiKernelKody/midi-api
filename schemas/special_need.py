from pydantic import BaseModel

class SpecialNeedBase(BaseModel):
    name: str
    description: str

class SpecialNeedCreate(SpecialNeedBase):
    pass

class SpecialNeedUpdate(SpecialNeedBase):
    pass

class SpecialNeedInDBBase(SpecialNeedBase):
    id: int

    class Config:
        orm_mode = True

class SpecialNeed(SpecialNeedInDBBase):
    pass

class SpecialNeedInDB(SpecialNeedInDBBase):
    pass
