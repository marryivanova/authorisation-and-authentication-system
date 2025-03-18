from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    role: str

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    username: str
    role: str
