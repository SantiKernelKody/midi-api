from pydantic import BaseModel

class UserRoleBase(BaseModel):
    name: str
    display_name: str
    description: str

class UserRoleCreate(UserRoleBase):
    pass

class UserRoleUpdate(UserRoleBase):
    pass

class UserRoleInDBBase(UserRoleBase):
    id: int

    class Config:
         from_attributes = True

class UserRole(UserRoleInDBBase):
    pass

class UserRoleInDB(UserRoleInDBBase):
    pass
