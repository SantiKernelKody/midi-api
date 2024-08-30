from pydantic import BaseModel
from datetime import datetime

class EducationalEntityBase(BaseModel):
    #id: int
    name: str
    code: str
    description: str

class EducationalEntityCreate(EducationalEntityBase):
    pass

class EducationalEntityUpdate(EducationalEntityBase):
    pass

class EducationalEntityInDBBase(EducationalEntityBase):
    id: int
    #created_at: datetime

    

class EducationalEntity(EducationalEntityInDBBase):
    id: int
    class Config:
        orm_mode = True
        from_attributes = True
    pass

class EducationalEntityInDB(EducationalEntityInDBBase):
    pass
