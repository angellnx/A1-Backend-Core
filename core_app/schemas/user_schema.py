from pydantic import BaseModel, EmailStr

class UserRequest(BaseModel):
    email: EmailStr
    name: str
    username: str
    password: str
    phone: str | None = None

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    username: str
    phone: str | None = None
    # password nunca aparece na response