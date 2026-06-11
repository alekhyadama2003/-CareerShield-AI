from fastapi import FastAPI, UploadFile, File
from backend.job_matcher import calculate_match
import shutil
import os
import fitz

app = FastAPI()

UPLOAD_FOLDER = "uploads"

SKILLS_DB = [
    "Java",
    "Python",
    "SQL",
    "Spring Boot",
    "REST API",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Git",
    "GitHub",
    "Maven",
    "DSA",
    "DBMS",
    "OOP",
    "Computer Networks"
]

def extract_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


@app.get("/")
def home():
    return {
        "project": "CareerShield AI",
        "message": "Workforce Intelligence for the AI Era"
    }


@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = ""

    if file.filename.endswith(".pdf"):
        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

    skills = extract_skills(text)

    return {
        "filename": file.filename,
        "skills": skills,
        "resume_text": text[:1000]
    }
@app.post("/match-job")
async def match_job(job_skills: list[str]):
    
    resume_skills = [
        "Python",
        "SQL",
        "FastAPI",
        "Git"
    ]

    result = calculate_match(resume_skills, job_skills)

    return result