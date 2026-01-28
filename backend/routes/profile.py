from fastapi import APIRouter, Depends
from config.db import db
from utils.jwt_dependency import get_current_user   

router = APIRouter()

users_col = db["users"]
vault_col = db["certificates"]

# 1️⃣ GET PROFILE + CERTS
@router.get("/profile/me")
def get_my_profile(email: str = Depends(get_current_user)):
    user = users_col.find_one(
        {"email": email},
        {"_id": 0, "password": 0}
    )

    certs = list(
        vault_col.find(
            {"user_id": email},
            {"_id": 0}
        ).sort("uploaded_at", -1)
    )

    return {
        "user": user,
        "certificates": certs
    }


# 2️⃣ UPDATE PROFILE
@router.put("/profile/update")
def update_profile(
    data: dict,
    email: str = Depends(get_current_user)
):
    users_col.update_one(
        {"email": email},
        {"$set": data}
    )
    return {"status": "updated"}


