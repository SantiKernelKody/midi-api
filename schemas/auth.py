from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    rawpassword: str
    role_name: str
class SignupRequest(BaseModel):
    name: str
    last_name: str
    rawpassword: str
    email: str
    token: str