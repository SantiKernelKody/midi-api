from pydantic import BaseModel

class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass

class CityInDBBase(CityBase):
    id: int

    class Config:
        orm_mode = True

class City(CityInDBBase):
    pass
