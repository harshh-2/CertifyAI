import fitz  # PyMuPDF
import re

def get_text_from_pdf(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    # Extract text and join lines with spaces to fix hyphenated words
    text = " ".join([page.get_text() for page in doc])
    # Remove extra whitespace and newlines
    return " ".join(text.split())

def extract_skills_robust(resume_text, db_skills):
    found_skills = []
    
    # Lowercase everything for case-insensitive matching
    resume_text = resume_text.lower()
    
    for skill in db_skills:
        # This Regex is the "Secret Sauce":
        # \b ensures we match 'Java' but NOT the 'Java' inside 'Javascript'
        # re.escape handles special characters like C++ or .NET
        pattern = rf'\b{re.escape(skill.lower())}\b'
        
        if re.search(pattern, resume_text):
            found_skills.append(skill)
            
    return sorted(list(set(found_skills)))