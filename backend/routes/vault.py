from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from config.db import db
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from datetime import datetime
import hashlib
import os
from io import BytesIO

import pdfplumber
from PIL import Image
import pytesseract

# NEW imports
from utils.provider_map import PROVIDER_MAP
from utils.skill_map import SKILL_MAP

router = APIRouter()

vault_col = db["certificates"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")


# ---------------- AUTH ----------------

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------- HELPERS ----------------

def extract_text(file: UploadFile, content: bytes):

    if file.filename.lower().endswith(".pdf"):
        with pdfplumber.open(BytesIO(content)) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text

    image = Image.open(BytesIO(content))
    return pytesseract.image_to_string(image)


def detect_title(text: str):
    lines = [l.strip() for l in text.split("\n") if len(l.strip()) > 6]
    if lines:
        return lines[0][:120]
    return "Unnamed Certificate"


# NEW — Provider detection
def detect_provider(text: str):
    text = text.lower()
    for k, v in PROVIDER_MAP.items():
        if k in text:
            return v
    return "Unknown"


# NEW — Skill extraction
def extract_skills(text: str):
    text = text.lower()
    found = []

    for k, v in SKILL_MAP.items():
        if k in text:
            found.append({
                "name": v,
                "confidence": 0.8
            })

    return found


# ---------------- ROUTES ----------------

@router.post("/vault/upload")
async def upload_certificate(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):

    content = await file.read()

    file_hash = hashlib.sha256(content).hexdigest()

    # Duplicate check per user
    if vault_col.find_one({"user_id": user_id, "file_hash": file_hash}):
        return {"status": "duplicate"}

    extracted_text = extract_text(file, content)
    title = detect_title(extracted_text)

    # NEW
    provider = detect_provider(extracted_text)
    skills = extract_skills(extracted_text)

    doc = {
        "user_id": user_id,
        "original_filename": file.filename,
        "certificate_name": title,
        "provider": provider,
        "skills": skills,
        "raw_text": extracted_text,
        "file_hash": file_hash,
        "uploaded_at": datetime.utcnow()
    }

    vault_col.insert_one(doc)

    return {
        "status": "uploaded",
        "certificate_name": title,
        "provider": provider,
        "skills": skills
    }


@router.get("/vault/my-certificates")
def get_my_certificates(user_id: str = Depends(get_current_user)):

    certs = list(
        vault_col.find(
            {"user_id": user_id},
            {"_id": 0}
        ).sort("uploaded_at", -1)
    )

    return {
        "total": len(certs),
        "certificates": certs
    }
