# AI-Based Resume Skill Analyzer

An AI-powered resume analyzer that compares real resumes (PDF/DOCX) with job roles or job descriptions and performs explainable skill-gap analysis similar to an ATS system.

Features
- Upload real resumes (PDF or Word)
- Extracts only the **Skills** section
- Role-based skill suggestions (Hybrid approach)
- Skill normalization (AWS/Azure/GCP → atomic skills)
- User confirmation before analysis
- Skill match percentage & missing skills
- User-friendly design (Google Colab)

Tech Stack
- Python
- NLP (NLTK)
- pdfplumber
- python-docx
- Google Colab

How It Works
1. Upload resume (PDF/DOCX)
2. Enter job role
3. Review suggested skills
4. Edit or confirm skills
5. Get skill match percentage and gap analysis

Example Output
Skill Match Percentage: 33.33%
Matched Skills: Python, Java, SQL
Missing Skills: REST APIs, Microservices, MongoDB

Use Cases
- Resume screening
- Skill-gap analysis
- Career planning
- ATS-style matching simulation

Future Improvements
- TF-IDF + cosine similarity
- Learning roadmap generation
- Web UI (Flask / Streamlit)

Note
This project is designed to run on **Google Colab** for interactive resume upload.

