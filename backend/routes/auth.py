from fastapi import APIRouter, HTTPException
from models.user import UserLogin
from utils.auth_utils import verify_password, create_access_token
from config.db import user_col

router = APIRouter(
    tags=["Authentication"]
)

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
    