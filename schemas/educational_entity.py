from pydantic import BaseModel
from datetime import datetime

class EducationalEntityBase(BaseModel):
    id: int
    name: str
    description: str

class EducationalEntityCreate(EducationalEntityBase):
    pass

class EducationalEntityUpdate(EducationalEntityBase):
    pass

class EducationalEntityInDBBase(EducationalEntityBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class EducationalEntity(EducationalEntityInDBBase):
    pass

class EducationalEntityInDB(EducationalEntityInDBBase):
    pass
