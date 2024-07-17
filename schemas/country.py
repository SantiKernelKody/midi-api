from pydantic import BaseModel

class CountryBase(BaseModel):
    name: str

class CountryCreate(CountryBase):
    pass

class CountryUpdate(CountryBase):
    pass

class CountryInDBBase(CountryBase):
    id: int

    class Config:
        orm_mode = True

class Country(CountryInDBBase):
    pass
