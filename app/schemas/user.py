from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    role: str = "user"


class UserResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True