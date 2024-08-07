from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    rawpassword: str
    role_name: str
