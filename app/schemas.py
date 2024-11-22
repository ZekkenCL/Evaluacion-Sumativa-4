from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    surname: str
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: str
    is_deleted: bool

    class Config:
        orm_mode = True
