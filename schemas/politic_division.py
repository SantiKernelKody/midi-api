from pydantic import BaseModel

class PoliticDivisionBase(BaseModel):
    name: str

class PoliticDivisionCreate(PoliticDivisionBase):
    pass

class PoliticDivisionUpdate(PoliticDivisionBase):
    pass

class PoliticDivisionInDBBase(PoliticDivisionBase):
    id: int

    class Config:
        orm_mode = True

class PoliticDivision(PoliticDivisionInDBBase):
    pass
