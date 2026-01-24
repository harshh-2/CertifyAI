from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/register")
def register(user: dict):
    return {
        "message": "User registered successfully",
        "user": user
    }

@router.post("/login")
def login(credentials: dict):
    return {
        "message": "Login successful",
        "credentials": credentials
    }

