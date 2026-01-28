from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from config.db import db
from datetime import datetime
import hashlib
from io import BytesIO
import uuid
from utils.jwt_dependency import get_current_user
import pdfplumber
from PIL import Image
import pytesseract

from utils.provider_map import PROVIDER_MAP
from utils.skill_map import SKILL_MAP

router = APIRouter()

vault_col = db["certificates"]

UPLOAD_DIR = "uploads/certificates"
##os.makedirs(UPLOAD_DIR, exist_ok=True)

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


def detect_provider(text: str):
    text = text.lower()
    for k, v in PROVIDER_MAP.items():
        if k in text:
            return v
    return "Unknown"


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

    # Duplicate check
    if vault_col.find_one({"user_id": user_id, "file_hash": file_hash}):
        return {"status": "duplicate"}

    extracted_text = extract_text(file, content)
    title = detect_title(extracted_text)
    provider = detect_provider(extracted_text)
    skills = extract_skills(extracted_text)

    # Save file physically
    ext = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as f:
        f.write(content)

    doc = {
        "user_id": user_id,
        "original_filename": file.filename,
        "certificate_name": title,
        "provider": provider,
        "skills": skills,
        "raw_text": extracted_text,
        "file_hash": file_hash,
        "file_path": file_path,
            "file_path": file_path,   # pdf preview line

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


@router.get("/vault/view/{filename}")
def view_certificate(filename: str, user_id: str = Depends(get_current_user)):

    cert = vault_col.find_one({
        "user_id": user_id,
        "file_path": {"$regex": filename}
    })

    if not cert:
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(cert["file_path"])
