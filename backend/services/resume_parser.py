import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def parse_skills(text, known_skills):
    # known_skills is a list of skills from your Cloud Atlas DB
    found_skills = []
    
    # Convert text to lowercase for easier matching
    text_lower = text.lower()
    
    for skill in known_skills:
        # Use regex to find the skill as a whole word (so "Java" doesn't match "Javascript")
        if re.search(rf'\b{re.escape(skill.lower())}\b', text_lower):
            found_skills.append(skill)
            
    return list(set(found_skills)) # Remove duplicates
