import fitz
import re

# This map ensures messy user input is converted to your DB's standard naming
ALIAS_MAP = {
    "Python": ["py", "python3", "python2", "pip"],
    "JavaScript": ["js", "es6", "javascript.js", "ecmascript"],
    "TypeScript": ["ts", "type script"],
    "C++": ["cplusplus", "cpp", "c plus plus"],
    "C#": ["csharp", "c sharp", "dotnet", ".net"],
    "Ruby": ["rb", "ruby on rails", "ror"],
    "Go": ["golang", "go language", "go lang"],
    "React": ["reactjs", "react.js", "react native"],
    "Angular": ["angularjs", "angular.js", "ng"],
    "Vue": ["vuejs", "vue.js"],
    "Node.js": ["nodejs", "node.js", "node js", "node"],
    "Express": ["expressjs", "express.js"],
    "MongoDB": ["mongo", "nosql", "mongodb"],
    "PostgreSQL": ["postgres", "psql", "postgresql"],
    "Machine Learning": ["ml", "machinelearning"],
    "Artificial Intelligence": ["ai", "genai", "generative ai"],
    "Deep Learning": ["dl", "neural networks"],
    "Scikit-Learn": ["sklearn", "scikit"],
    "TensorFlow": ["tf"],
    "PyTorch": ["torch"],
    "NLP": ["natural language processing"],
    "AWS": ["amazon web services", "amazon cloud" , "aws fundamentals"],
    "GCP": ["google cloud platform", "google cloud"],
    "Azure": ["microsoft azure"],
    "Kubernetes": ["k8s", "kube"],
    "Docker": ["containers", "docker"],
    "CI/CD": ["continuous integration", "continuous deployment", "jenkins", "github actions"],
    "HTML": ["html5"],
    "CSS": ["css3", "tailwind", "bootstrap", "sass"]
}

def get_text_from_pdf(file_bytes):
    """Extracts and cleans text from a PDF file."""
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = " ".join([page.get_text() for page in doc])
        return " ".join(text.split())
    except Exception as e:
        print(f"Error parsing PDF: {e}")
        return ""

def extract_skills_robust(resume_text, db_skills):
    """Matches text against ALIAS_MAP and DB skills for chatbot-ready output."""
    # 1. Prepare text versions
    # We keep + and # for C++ and C#
    clean_resume = re.sub(r'[^a-zA-Z0-9\s\+#]', ' ', resume_text).lower()
    compressed_resume = re.sub(r'\s+', '', clean_resume)
    
    found_skills = set()
    
    # --- PART A: Check the Alias Map First (Normalization) ---
    for standard_name, aliases in ALIAS_MAP.items():
        # Check standard name AND all its aliases
        variants = [standard_name.lower()] + [a.lower() for a in aliases]
        for variant in variants:
            # Check for whole word match or compressed match
            pattern = rf'\b{re.escape(variant)}\b'
            variant_compressed = variant.replace(" ", "")
            
            if re.search(pattern, clean_resume) or (len(variant_compressed) > 2 and variant_compressed in compressed_resume):
                found_skills.add(standard_name) # Add the pretty version (e.g., "JavaScript")
                break

    # --- PART B: Check DB Skills (For everything else) ---
    for skill in db_skills:
        original_skill = skill.strip()
        skill_clean = re.sub(r'[^a-zA-Z0-9\+#\s]', '', original_skill).lower().strip()
        
        if not skill_clean: 
            continue

        pattern = rf'\b{re.escape(skill_clean)}\b'
        skill_compressed = skill_clean.replace(" ", "")
        
        if re.search(pattern, clean_resume) or (len(skill_compressed) > 2 and skill_compressed in compressed_resume):
            found_skills.add(original_skill)
            
    return sorted(list(found_skills))