from fastapi import APIRouter, HTTPException
from models.user import UserLogin
from utils.auth_utils import verify_password, create_access_token
from config.db import user_col
from models.user import UserSignup
from utils.auth_utils import hash_password, create_access_token
from fastapi import HTTPException, status
from datetime import datetime

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):

    # 1️⃣ Check existing user
    existing_user = await user_col.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # 2️⃣ Hash password
    hashed_password = hash_password(user.password)

    # 3️⃣ Build MongoDB document
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "profile": {
            "year_of_college": user.year_of_college,
            "age": user.age,
            "institution": user.institution,
            "gender": user.gender
        },
        "role": "user",
        "created_at": datetime.utcnow()
    }

    # 4️⃣ Insert into DB
    await user_col.insert_one(new_user)

    # 5️⃣ (Optional) Auto-login after signup
    token = create_access_token({"sub": user.email})

    return {
        "message": "Account created successfully",
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login")
async def login(user: UserLogin):
    # 1. Find user by email
    db_user = await user_col.find_one({"email": user.email})
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 2. Verify password
    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # 3. Create JWT token
    token = create_access_token({
        "sub": str(db_user["_id"]),
        "email": db_user["email"]
    })

    # 4. Return response to frontend
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "username": db_user["username"],
            "email": db_user["email"]
        }
    }
    