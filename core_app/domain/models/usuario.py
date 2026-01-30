from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    id_usuario: int
    ds_username: str
    nm_usuario: str
    ds_email: EmailStr
    ds_telefone: str
    ds_senha: str
