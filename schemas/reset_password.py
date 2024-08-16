from pydantic import BaseModel

# Definir un esquema para el cuerpo de la solicitud
class ResetPasswordRequest(BaseModel):
    email: str

class ResetPasswordData(BaseModel):
    token: str
    new_password: str