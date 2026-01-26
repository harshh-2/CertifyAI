from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserSignup(BaseModel):
    username: str

    email: EmailStr

    password: str = Field(..., min_length=6)

    # age between 13 and 100
    age: int = Field(..., ge=13, le=100)

    # college year between 1 and 6
    year_of_college: int = Field(..., ge=1, le=6)

    institution: str

    # restrict gender values
    gender: str = Field(..., pattern="^(male|female|other)$")


class UserLogin(BaseModel):
    email: EmailStr
    password: str
