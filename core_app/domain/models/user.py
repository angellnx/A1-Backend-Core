from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    username: str
    name: str
    email: EmailStr
    phone: str | None = None
    password: str
