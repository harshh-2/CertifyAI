from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    year_of_college: int
    age: int
    institution: str
    gender: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

