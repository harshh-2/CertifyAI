import re
from fastapi import APIRouter, UploadFile, File
from config.db import cert_col
from services.resume_parser import get_text_from_pdf, extract_skills_robust

router = APIRouter()

# 1. ADD THE HELPER FUNCTION HERE (At the top)
def calculate_match_score(user_skills, cert_skills_str):
    # Handles empty strings or None values
    if not cert_skills_str:
        return 0.0, []
        
    cert_skills = [s.strip().lower() for s in re.split(r'[,;]+', cert_skills_str)]
    user_skills_set = set([s.lower() for s in user_skills])
    
    # Skills the user ALREADY HAS
    matches = [s for s in cert_skills if s in user_skills_set]
    
    # Skills the user IS MISSING (The Gap)
    missing = [s for s in cert_skills if s not in user_skills_set]
    
    score = (len(matches) / len(cert_skills)) * 100
    return round(score, 2), matches, missing

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    content = await file.read()
    text = get_text_from_pdf(content)
    
    # Logic to get unique skills from DB (as we did before)
    raw_db_skills = await cert_col.distinct("Skill")
    all_skills = set()
    for s in raw_db_skills:
        if s:
            parts = re.split(r'[,;]+', s)
            for p in parts: all_skills.add(p.strip())
    
    matched = extract_skills_robust(text, list(all_skills))
    
    # Fetch data from MongoDB
    recommendations = []
    async for cert in cert_col.find({"Skill": {"$regex": "|".join(matched), "$options": "i"}}).limit(10):
        cert["_id"] = str(cert["_id"])
        recommendations.append(cert)

    # 2. ADD THE LOOP LOGIC HERE (Before the return)
    final_results = []
    for cert in recommendations:
        score, matching_parts, missing_parts = calculate_match_score(matched, cert.get("Skill", ""))
        
        # Inject the new AI fields into the dictionary
        cert["match_score"] = score
        cert["matching_skills"] = matching_parts
        cert["missing_skills"] = missing_parts
        
        # Add a "Recommendation Label"
        if score == 100:
            cert["label"] = "Perfect Match"
        elif score >= 50:
            cert["label"] = "Highly Recommended"
        else:
            cert["label"] = "Skill Upward"
            
        final_results.append(cert)

    # 3. SORT BY SCORE
    final_results.sort(key=lambda x: x['match_score'], reverse=True)

    return {
        "filename": file.filename,
        "detected_skills": matched,
        "recommendations": final_results
    }