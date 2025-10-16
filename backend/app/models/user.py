from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    name: str
    timezone: str = "America/Los_Angeles"


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    timezone: Optional[str] = None


class User(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    timezone: str
    created_at: datetime

