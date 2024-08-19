from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class PlayerBase(BaseModel):
    full_name: str
    edad: int
    ethnicity: Optional[str] = None
    special_need_description: Optional[str] = None
    special_need: Optional[int] = None

class PlayerCreate(PlayerBase):
    pass

class PlayerUpdate(PlayerBase):
    pass

class PlayerInDBBase(PlayerBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class Player(PlayerInDBBase):
    class Config:
        from_attributes = True

class PlayerInDB(PlayerInDBBase):
    pass

class PlayerDetailSchema(BaseModel):
    full_name: str
    edad: int
    ethnicity: str
    caretaker_name: str
    caretaker_email: str

    class Config:
        orm_mode = True

class PlayerWithCaretaker(BaseModel):
    full_name: str = Field(None, description="Full name of the player")
    edad: int = Field(None, description="Age of the player")
    ethnicity: Optional[str] = Field(None, description="Ethnicity of the player")
    caretaker_email: Optional[EmailStr] = Field(None, description="Email of the caretaker")

    class Config:
        orm_mode = True