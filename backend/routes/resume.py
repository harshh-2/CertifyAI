
from fastapi import APIRouter, UploadFile, File, Depends
from datetime import datetime
from io import BytesIO
import pdfplumber
import hashlib

from config.db import db
from utils.jwt_dependency import get_current_user
from utils.skill_map import SKILL_MAP

router = APIRouter()

resume_col = db["resumes"]

def extract_text(content):
    with pdfplumber.open(BytesIO(content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text


def extract_skills(text):
    text = text.lower()
    skills = []

    for k, v in SKILL_MAP.items():
        if k in text:
            skills.append(v)

    return list(set(skills))


@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user)
):

    content = await file.read()
    text = extract_text(content)

    skills = extract_skills(text)

    resume_col.insert_one({
        "user_id": user_id,
        "filename": file.filename,
        "skills": skills,
        "raw_text": text,
        "uploaded_at": datetime.utcnow()
    })

    return {
        "status": "uploaded",
        "skills": skills
    }
