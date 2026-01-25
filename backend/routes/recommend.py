import re
from fastapi import APIRouter, UploadFile, File, Body, HTTPException
from config.db import cert_col
from typing import List
from services.resume_parser import get_text_from_pdf, extract_skills_robust
from config.path import CAREER_PATHS

router = APIRouter()

# --- HELPER FUNCTIONS ---
def calculate_match_score(user_skills, cert_skills_str):
    if not cert_skills_str:
        return 0.0, []
    cert_skills = [s.strip().lower() for s in re.split(r'[,;]+', cert_skills_str)]
    user_skills_set = set([s.lower() for s in user_skills])
    matches = [s for s in cert_skills if s in user_skills_set]
    missing = [s for s in cert_skills if s not in user_skills_set]
    score = (len(matches) / len(cert_skills)) * 100 if cert_skills else 0
    return round(score, 2), matches, missing

# --- ENDPOINTS ---

# NEW: Use this to populate the checkboxes when a user selects a path
@router.get("/path-skills/{path_name}")
async def get_path_skills(path_name: str):
    if path_name not in CAREER_PATHS:
        raise HTTPException(status_code=404, detail="Path not found")
    return {"path": path_name, "skills": CAREER_PATHS[path_name]}

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = get_text_from_pdf(content)
    
    cursor = cert_col.find({}, {"Skill": 1, "_id": 0})
    all_db_skills = set()
    async for doc in cursor:
        skill_field = doc.get("Skill", "")
        if skill_field:
            parts = re.split(r'[,;/|\n]+', skill_field)
            for p in parts:
                if p.strip(): all_db_skills.add(p.strip())

    matched = extract_skills_robust(text, list(all_db_skills))
    
    if not matched:
        return {"filename": file.filename, "detected_skills": [], "message": "No skills found."}

    recommendations = []
    regex_pattern = "|".join([re.escape(s) for s in matched])
    
    async for cert in cert_col.find({"Skill": {"$regex": regex_pattern, "$options": "i"}}).limit(20):
        cert["_id"] = str(cert["_id"])
        score, matching, missing = calculate_match_score(matched, cert.get("Skill", ""))
        cert.update({
            "match_score": score,
            "matching_skills": matching,
            "missing_skills": missing
        })
        recommendations.append(cert)

    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    return {"filename": file.filename, "detected_skills": matched, "recommendations": recommendations}

@router.post("/recommend-by-path")
async def recommend_by_path(
    selected_path: str, 
    detected_skills: List[str] = Body(...) 
):
    if selected_path not in CAREER_PATHS:
        return {"error": "Invalid path selection"}

    required_skills = CAREER_PATHS[selected_path]
    user_skills_set = set([s.lower() for s in detected_skills])
    
    matching = [s for s in required_skills if s.lower() in user_skills_set]
    missing = [s for s in required_skills if s.lower() not in user_skills_set]
    
    recommendations = []
    if missing:
        regex_pattern = "|".join([re.escape(s) for s in missing])
        async for cert in cert_col.find({"Skill": {"$regex": regex_pattern, "$options": "i"}}).limit(7):
            cert["_id"] = str(cert["_id"])
            # Re-calculate score specifically for this cert vs user skills
            score, m, mis = calculate_match_score(detected_skills, cert.get("Skill", ""))
            cert.update({"match_score": score, "matching_skills": m, "missing_skills": mis})
            recommendations.append(cert)

    return {
        "path": selected_path,
        "matching_skills": matching,
        "missing_skills": missing,
        "recommendations": sorted(recommendations, key=lambda x: x['match_score'], reverse=True)
    }