from flask import Flask, render_template, request, jsonify
import pdfplumber
from docx import Document
import re

app = Flask(__name__)

# ------------------------------------------------
# SKILL DATABASE
# ------------------------------------------------

SKILLS_DB = {

# Programming
"python","java","cpp","csharp","golang","rust",
"javascript","typescript",

# Web
"html","css","react","angular","vue","nextjs","bootstrap","tailwind",

# Backend
"nodejs","express","django","flask","spring",
"grpc","graphql","rest","websockets","microservices",

# Databases
"sql","mysql","postgresql","mongodb","neo4j","redis",

# DevOps
"docker","kubernetes","terraform","jenkins","cicd",

# Cloud
"aws","gcp","azure","ec2","s3","cloudwatch",

# Messaging
"kafka","pubsub","redisstreams",

# AI/ML
"machinelearning","deeplearning","nlp","computervision",
"tensorflow","pytorch","scikitlearn",
"pandas","numpy",

# Tools
"git","github","linux","bash","postman","jest",

# Fundamentals
"datastructures","algorithms","dbms",
"operatingsystems","computernetworks",

# Analytics
"tableau","powerbi","excel","statistics"
}

# ------------------------------------------------
# ROLE SKILLS
# ------------------------------------------------

ROLE_SKILLS = {

"software engineer":[
"datastructures","algorithms","dbms","operatingsystems","computernetworks",
"python","java","cpp","golang","javascript","typescript",
"nodejs","express","rest","grpc","graphql","microservices",
"sql","postgresql","mongodb","redis",
"docker","kubernetes","cicd",
"aws","gcp","git"
],

"backend developer":[
"python","java","golang","nodejs","express",
"rest","grpc","graphql","microservices",
"sql","postgresql","mongodb","redis",
"docker","kubernetes","cicd",
"aws","gcp","linux","git"
],

"frontend developer":[
"html","css","javascript","typescript",
"react","angular","vue","nextjs",
"bootstrap","tailwind","git"
],

"full stack developer":[
"html","css","javascript","react","nextjs",
"nodejs","express","rest","graphql",
"mongodb","postgresql","sql",
"docker","git"
],

"ai/ml engineer":[
"python","machinelearning","deeplearning","nlp","computervision",
"tensorflow","pytorch","scikitlearn",
"pandas","numpy","sql","git"
],

"data scientist":[
"python","machinelearning","pandas","numpy",
"statistics","sql","dataanalysis",
"tableau","powerbi"
],

"data analyst":[
"python","sql","excel","tableau","powerbi",
"statistics","dataanalysis"
],

"devops engineer":[
"docker","kubernetes","terraform","jenkins","cicd",
"aws","gcp","linux","bash","git"
],

"cloud engineer":[
"aws","gcp","azure",
"docker","kubernetes","terraform",
"linux","networking"
],

"mobile developer":[
"java","kotlin","swift","flutter",
"reactnative","firebase"
],

"game developer":[
"cpp","csharp","unity","unrealengine"
],

"cybersecurity engineer":[
"networksecurity","ethicalhacking",
"penetrationtesting","cryptography",
"linux","python"
],

"database engineer":[
"sql","mysql","postgresql","mongodb",
"redis","databasedesign"
]

}

# ------------------------------------------------
# TEXT NORMALIZATION
# ------------------------------------------------

def preprocess(text):

    text = text.lower()

    text = text.replace("c++","cpp")
    text = text.replace("c#","csharp")
    text = text.replace("node.js","nodejs")
    text = text.replace("ci/cd","cicd")
    text = text.replace("machine learning","machinelearning")
    text = text.replace("deep learning","deeplearning")
    text = text.replace("data structures","datastructures")
    text = text.replace("computer networks","computernetworks")
    text = text.replace("operating systems","operatingsystems")

    text = re.sub(r"[•/,+()|]", " ", text)

    text = re.sub(r"[^\w\s]", " ", text)

    return text

# ------------------------------------------------
# EXTRACT PDF
# ------------------------------------------------

def extract_pdf(path):

    text=""

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            if page.extract_text():
                text += page.extract_text()

    return text

# ------------------------------------------------
# EXTRACT DOCX
# ------------------------------------------------

def extract_docx(path):

    doc = Document(path)

    return "\n".join(p.text for p in doc.paragraphs)

# ------------------------------------------------
# SKILL EXTRACTION
# ------------------------------------------------

def extract_skills(text):

    found=set()

    for skill in SKILLS_DB:

        pattern=r"\b"+re.escape(skill)+r"\b"

        if re.search(pattern,text):

            found.add(skill)

    return found

# ------------------------------------------------
# SCORE CALCULATION
# ------------------------------------------------

def compute_score(resume_skills, role_skills):

    fundamentals = {
        "datastructures",
        "algorithms",
        "dbms",
        "operatingsystems",
        "computernetworks"
    }

    resume_skills = set(resume_skills)
    role_skills = set(role_skills)

    matched = resume_skills & role_skills
    missing = role_skills - resume_skills

    # Split skills
    role_fund = role_skills & fundamentals
    role_tech = role_skills - fundamentals

    matched_fund = resume_skills & role_fund
    matched_tech = resume_skills & role_tech

    # Calculate scores
    fund_score = len(matched_fund) / len(role_fund) if role_fund else 1
    tech_score = len(matched_tech) / len(role_tech) if role_tech else 1

    # Weighted combination
    score = (0.3 * fund_score + 0.7 * tech_score) * 100

    return matched, missing, round(score,2)
# ------------------------------------------------
# ROUTES
# ------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze",methods=["POST"])
def analyze():

    file=request.files["resume"]
    role=request.form["role"]

    path="uploaded_resume"

    file.save(path)

    if file.filename.endswith(".pdf"):
        text=extract_pdf(path)
    else:
        text=extract_docx(path)

    text=preprocess(text)

    resume_skills=extract_skills(text)

    role_skills=ROLE_SKILLS.get(role,[])

    matched,missing,score=compute_score(resume_skills,role_skills)

    return jsonify({

        "score":score,
        "matched":list(matched),
        "missing":list(missing)

    })

# ------------------------------------------------
# RUN SERVER
# ------------------------------------------------

if __name__=="__main__":
    app.run(debug=True)