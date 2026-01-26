import fitz
import re

# This map ensures messy user input is converted to your DB's standard naming
ALIAS_MAP = {

    # ================= CORE LANGUAGES =================
    "Python": [
        "py", "python3", "python2", "cpython", "pip", "pip3",
        "virtualenv", "venv", "anaconda", "miniconda"
    ],

    "Java": [
        "java8", "java11", "java17", "jdk", "jre", "spring",
        "spring boot", "springboot", "hibernate", "maven", "gradle"
    ],

    "JavaScript": [
        "js", "javascript.js", "es5", "es6", "es7", "ecmascript",
        "vanilla js", "vanilla javascript"
    ],

    "TypeScript": [
        "ts", "type script", "typescript.js"
    ],

    "C": [
        "clang", "gcc", "gnu c", "ansi c"
    ],

    "C++": [
        "cplusplus", "cpp", "c plus plus", "cxx",
        "stl", "boost"
    ],

    "C#": [
        "csharp", "c sharp", ".net", "dotnet",
        "asp.net", "asp.net core"
    ],

    "Go": [
        "golang", "go language", "go lang"
    ],

    "Rust": [
        "rustlang", "cargo"
    ],

    "Kotlin": [
        "kotlinlang", "android kotlin"
    ],

    "Swift": [
        "swiftui", "ios swift"
    ],

    "Ruby": [
        "rb", "ruby on rails", "rails", "ror"
    ],

    "PHP": [
        "php8", "laravel", "symfony", "codeigniter"
    ],

    "Scala": [
        "scala lang", "akka", "spark scala"
    ],

    "R": [
        "r language", "rstats"
    ],

    # ================= FRONTEND =================
    "HTML": [
        "html5", "markup", "hypertext markup language"
    ],

    "CSS": [
        "css3", "tailwind", "bootstrap", "sass", "scss",
        "less", "postcss"
    ],

    "React": [
        "reactjs", "react.js", "jsx", "tsx",
        "react native", "next.js", "nextjs"
    ],

    "Angular": [
        "angularjs", "angular.js", "ng"
    ],

    "Vue": [
        "vuejs", "vue.js", "nuxt", "nuxt.js"
    ],

    "Svelte": [
        "sveltekit", "svelte.js"
    ],

    "jQuery": [
        "jquery.js"
    ],

    # ================= BACKEND =================
    "Node.js": [
        "nodejs", "node.js", "node", "npm", "yarn", "pnpm"
    ],

    "Express": [
        "expressjs", "express.js"
    ],

    "FastAPI": [
        "fast api", "fastapi framework"
    ],

    "Django": [
        "django rest", "django rest framework", "drf"
    ],

    "Flask": [
        "flask api"
    ],

    "Spring Boot": [
        "springboot", "spring boot java"
    ],

    # ================= DATABASES =================
    "MySQL": [
        "mysql8", "relational db"
    ],

    "PostgreSQL": [
        "postgres", "psql", "postgresql"
    ],

    "MongoDB": [
        "mongo", "nosql", "mongodb atlas"
    ],

    "Redis": [
        "redis cache", "in-memory db"
    ],

    "SQLite": [
        "sqlite3"
    ],

    "Oracle": [
        "oracle db", "plsql"
    ],

    "Cassandra": [
        "apache cassandra"
    ],

    # ================= DATA & AI =================
    "Machine Learning": [
        "ml", "machinelearning", "supervised learning",
        "unsupervised learning", "reinforcement learning"
    ],

    "Artificial Intelligence": [
        "ai", "genai", "generative ai", "artificial intelligence"
    ],

    "Deep Learning": [
        "dl", "neural networks", "cnn", "rnn", "lstm"
    ],

    "NLP": [
        "natural language processing", "text mining",
        "text analytics"
    ],

    "Computer Vision": [
        "cv", "image processing"
    ],

    "Scikit-Learn": [
        "sklearn", "scikit"
    ],

    "TensorFlow": [
        "tf", "tensorflow keras"
    ],

    "PyTorch": [
        "torch", "pytorch lightning"
    ],

    "Pandas": [
        "pd", "dataframes"
    ],

    "NumPy": [
        "numpy arrays", "np"
    ],

    # ================= CLOUD =================
    "AWS": [
        "amazon web services", "amazon cloud",
        "ec2", "s3", "lambda", "cloudfront", "iam"
    ],

    "Azure": [
        "microsoft azure", "azure devops", "azure functions"
    ],

    "GCP": [
        "google cloud", "google cloud platform",
        "gke", "bigquery"
    ],

    # ================= DEVOPS =================
    "Docker": [
        "containers", "dockerfile", "docker compose"
    ],

    "Kubernetes": [
        "k8s", "kube", "helm"
    ],

    "CI/CD": [
        "continuous integration", "continuous deployment",
        "jenkins", "github actions", "gitlab ci", "circleci"
    ],

    "Terraform": [
        "iac", "infrastructure as code"
    ],

    "Ansible": [
        "configuration management"
    ],

    # ================= VERSION CONTROL =================
    "Git": [
        "git scm", "git cli"
    ],

    "GitHub": [
        "github repo", "github actions"
    ],

    "GitLab": [
        "gitlab ci"
    ],

    "Bitbucket": [
        "bitbucket pipelines"
    ],

    # ================= TESTING =================
    "Unit Testing": [
        "unittest", "pytest", "junit", "mocha"
    ],

    "Automation Testing": [
        "selenium", "playwright", "cypress"
    ],

    # ================= SYSTEM DESIGN =================
    "System Design": [
        "low level design", "lld",
        "high level design", "hld",
        "scalability", "distributed systems"
    ],

    "Microservices": [
        "service-oriented architecture", "soa"
    ],

    "REST API": [
        "restful services", "rest api"
    ],

    "GraphQL": [
        "apollo graphql"
    ],

    # ================= MOBILE =================
    "Android": [
        "android studio", "android sdk"
    ],

    "iOS": [
        "ios development", "iphone apps"
    ],

    "Flutter": [
        "dart flutter"
    ],

    "React Native": [
        "rn", "react native cli"
    ],

    # ================= OS / CS CORE =================
    "Operating Systems": [
        "os", "process scheduling", "deadlock"
    ],

    "Computer Networks": [
        "cn", "tcp/ip", "udp", "http", "https"
    ],

    "DBMS": [
        "database management systems"
    ],

    "OOP": [
        "object oriented programming",
        "inheritance", "polymorphism", "encapsulation"
    ],

    "DSA": [
        "data structures", "algorithms",
        "arrays", "linked list", "stack", "queue",
        "tree", "graph", "dp", "greedy"
    ]
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