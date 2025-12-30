import nltk
import string
import re
from nltk.corpus import stopwords
import pdfplumber
from docx import Document
from google.colab import files

try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [t for t in tokens if t not in stopwords.words("english")]
    return " ".join(tokens)

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_skill_section(resume_text):
    resume_text = resume_text.lower()

    skill_heads = ["skills", "technical skills", "key skills", "technologies"]
    stop_heads = [
        "education", "experience", "projects", "summary",
        "profile", "communication", "address", "certifications"
    ]

    lines = resume_text.split("\n")
    capture = False
    skill_lines = []

    for line in lines:
        clean = line.strip()
        if any(h in clean for h in skill_heads):
            capture = True
            continue
        if capture and any(h in clean for h in stop_heads):
            break
        if capture:
            skill_lines.append(clean)

    return " ".join(skill_lines)

def normalize_skills(skill_list):
    normalized = set()
    for skill in skill_list:
        skill = re.sub(r"\(.*?\)", "", skill)
        parts = re.split(r"/|,|\+", skill)
        for p in parts:
            clean = p.strip().lower()
            if clean:
                normalized.add(clean)
    return normalized

SKILLS_DB = {
    "python","java","c","c++","c#","go","sql","postgresql","mongodb",
    "machine learning","deep learning","nlp","data analysis",
    "data visualization","pandas","numpy","tensorflow","pytorch",
    "html5","css3","javascript","typescript","react","next.js","tailwind css",
    "node.js","rest apis","graphql","microservices","docker","kubernetes",
    "linux","bash","terraform","aws","azure","gcp",
    "unity","unreal engine","game physics","opengl","directx",
    "data structures","algorithms","statistics","scikit-learn"
}

def extract_skills(text):
    tokens = set(text.split())
    found = set()
    for skill in SKILLS_DB:
        if len(skill.split()) == 1:
            if skill in tokens:
                found.add(skill)
        else:
            if skill in text:
                found.add(skill)
    return found

def compare_skills(resume_skills, jd_skills):
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0
    return matched, missing, round(score, 2)

ROLE_SKILL_MAP = {
    "frontend developer": [
        "html5","css3","javascript (es6+)","typescript",
        "react","next.js","tailwind css","responsive design",
        "browser devtools","web performance"
    ],
    "backend developer": [
        "node.js","python","java","go","sql",
        "postgresql","mongodb","rest apis","graphql",
        "microservices","caching (redis)"
    ],
    "full stack developer": [
        "mern stack","mean stack","next.js","typescript",
        "restful apis","sql/nosql databases","git/github",
        "docker basics","cloud hosting (aws/vercel)"
    ],
    "devops engineer": [
        "linux/unix","docker","kubernetes","ci/cd (jenkins/github actions)",
        "terraform","ansible","cloud (aws/azure/gcp)",
        "bash/python scripting","monitoring","logging"
    ],
    "mobile app developer": [
        "react native","flutter","swift","kotlin",
        "dart","mobile ui/ux","firebase","api integration"
    ],
    "ai/ml engineer": [
        "python","pytorch","tensorflow","scikit-learn",
        "generative ai","llms","data engineering",
        "nlp","mlops","vector databases"
    ],
    "game developer": [
        "c++","c#","unity","unreal engine",
        "game physics","shaders/opengl","3d math","directx"
    ],
    "cloud engineer": [
        "aws/azure/gcp","serverless","cloud security",
        "iac (terraform)","networking","cost optimization","iam"
    ],
    "data scientist": [
        "python","r","sql","machine learning",
        "statistics","data visualization","pandas/numpy","spark"
    ],
    "cybersecurity engineer": [
        "network security","ethical hacking","siem",
        "cryptography","cloud security","incident response",
        "penetration testing","owasp top 10"
    ]
}

ROLE_ALIASES = {
    "software engineer":"backend developer",
    "software developer":"backend developer",
    "sde":"backend developer",
    "developer":"backend developer",
    "ml engineer":"ai/ml engineer"
}

print("📄 Please upload your resume (PDF or DOCX)")
uploaded = files.upload()

resume_path = list(uploaded.keys())[0]

if resume_path.endswith(".pdf"):
    resume_text = extract_text_from_pdf(resume_path)
elif resume_path.endswith(".docx"):
    resume_text = extract_text_from_docx(resume_path)
else:
    raise ValueError("Unsupported resume format")

role_input = input("\nEnter job role: ").lower()
role = ROLE_ALIASES.get(role_input, role_input)

if role in ROLE_SKILL_MAP:
    suggested = ROLE_SKILL_MAP[role]
    normalized = normalize_skills(suggested)

    print("\nSuggested skills:")
    print(", ".join(sorted(normalized)))

    edit = input("\nDo you want to EDIT these skills? (yes/no): ").lower()
    if edit == "yes":
        job_description = input("\nEnter final skills (comma-separated): ")
    else:
        job_description = " ".join(normalized)
else:
    print("\nRole not found. Paste full Job Description with skills:")
    job_description = input()

skill_section = extract_skill_section(resume_text)

resume_clean = preprocess_text(skill_section)
jd_clean = preprocess_text(job_description)

resume_skills = extract_skills(resume_clean)
jd_skills = extract_skills(jd_clean)

matched, missing, score = compare_skills(resume_skills, jd_skills)

print("\n🧑‍💼 Job Role:", role.title())
print("📊 Skill Match Percentage:", score, "%")
print("✅ Matched Skills:", matched)
print("❌ Missing Skills:", missing)
