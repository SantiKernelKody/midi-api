from pydantic import BaseModel

class UpdateUserData(BaseModel):
    name: str
    last_name: str
    email: str
from pydantic import BaseModel

class UpdatePasswordData(BaseModel):
    old_password: str
    new_password: str
