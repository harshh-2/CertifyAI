from fastapi import APIRouter, UploadFile, File
from backend.services.resume_parser import extract_text_from_pdf, parse_skills
from backend.config.db import cert_col

router = APIRouter()

@router.post("/parse-resume")
async def recommend_from_resume(file: UploadFile = File(...)):
    # 1. Read the uploaded file
    file_bytes = await file.read()
    resume_text = extract_text_from_pdf(file_bytes)
    
    # 2. Get unique skills from your Cloud Atlas to use as a "dictionary"
    # This makes sure we only look for skills we actually have certifications for
    db_skills = await cert_col.distinct("Skill") 
    # Note: If your skills are comma-separated strings like "Python, ML", 
    # you might need to split them first.
    
    # 3. Find matches
    matched_skills = parse_skills(resume_text, db_skills)
    
    # 4. Find certifications that match these skills in the Cloud DB
    recommendations = []
    async for cert in cert_col.find({"Skill": {"$in": matched_skills}}).limit(5):
        cert["_id"] = str(cert["_id"])
        recommendations.append(cert)
        
    return {
        "extracted_skills": matched_skills,
        "recommendations": recommendations
    }