import re
from fastapi import APIRouter, UploadFile, File, Body, HTTPException
from config.db import cert_col
from typing import List
from services.resume_parser import get_text_from_pdf, extract_skills_robust
from config.path import CAREER_PATHS
from fastapi import Depends
from utils.jwt_dependency import get_current_user


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
async def parse_resume(file: UploadFile = File(...),current_user: dict = Depends(get_current_user)):
    content = await file.read()
    text = get_text_from_pdf(content)
    current_user: dict = Depends(get_current_user)
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
async def recommend_by_path(selected_path: str, detected_skills: List[str] = Body(...) \):
    if selected_path not in CAREER_PATHS:
        return {"error": "Invalid path selection"}

    required_skills = [s.lower().strip() for s in CAREER_PATHS[selected_path]]
    user_skills_set = set(s.lower().strip() for s in detected_skills)
    total_path_count = len(required_skills)

    regex_pattern = "|".join(re.escape(s) for s in required_skills)
    recommendations = []
    
    async for cert in cert_col.find({"Skill": {"$regex": regex_pattern, "$options": "i"}}).limit(12):
        cert_skills_list = [s.strip().lower() for s in re.split(r'[,•|]+', cert.get("Skill", ""))]
        
        # Intersection of Cert skills and the specific Career Path
        relevant_in_cert = [s for s in cert_skills_list if s in required_skills]
        if not relevant_in_cert: continue

        to_learn = [s for s in relevant_in_cert if s not in user_skills_set]
        to_verify = [s for s in relevant_in_cert if s in user_skills_set]

        # CALCULATE IMPACT
        base_coverage = (len(relevant_in_cert) / total_path_count) * 100
        bonus = (15 + (len(to_learn) * 2)) if to_learn else 0
        final_score = min(round(base_coverage + bonus), 100)

        recommendations.append({
            "_id": str(cert["_id"]),
            "Certification": cert["Certification"],
            "Company": cert["Company"],
            "match_score": final_score,
            "to_learn": to_learn,
            "to_verify": to_verify
        })

    return {
        "stats": {
            "score": round((len(user_skills_set.intersection(set(required_skills))) / total_path_count) * 100),
            "count": len(user_skills_set.intersection(set(required_skills))),
            "total": total_path_count
        },
        "recommendations": sorted(recommendations, key=lambda x: x['match_score'], reverse=True)
    }