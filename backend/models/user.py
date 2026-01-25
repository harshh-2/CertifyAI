from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str

    year_of_college: Optional[int] = None
    age: Optional[int] = None
    institution: Optional[str] = None
    gender: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

