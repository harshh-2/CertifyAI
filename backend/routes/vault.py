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

    doc = {
        "user_id": user_id,
        "original_filename": file.filename,
        "detected_title": title,
        "file_hash": file_hash,
        "uploaded_at": datetime.utcnow()
    }

    vault_col.insert_one(doc)

    return {
        "status": "uploaded",
        "detected_title": title
    }


@router.get("/vault/my-certificates")
def get_my_certificates(user_id: str = Depends(get_current_user)):

    certs = list(vault_col.find(
        {"user_id": user_id},
        {"_id": 0}
    ))

    return certs
