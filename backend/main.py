from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil
import os
import fitz

from backend.database import SessionLocal, Job
from backend.job_matcher import calculate_match
from backend.ats_analyzer import calculate_ats_score
from backend.resume_reviewer import review_resume
from backend.career_recommender import recommend_careers
from backend.learning_tracker import learning_tracker



app = FastAPI()

# ---------------------------
# Upload folder setup
# ---------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---------------------------
# Skill extractor DB
# ---------------------------
SKILLS_DB = [
    "Java", "Python", "SQL", "Spring Boot", "REST API",
    "HTML", "CSS", "JavaScript", "React",
    "Git", "GitHub", "Maven",
    "DSA", "DBMS", "OOP", "Computer Networks"
]

def extract_skills(text):
    found_skills = []
    for skill in SKILLS_DB:
        if skill.lower() in text.lower():
            found_skills.append(skill)
    return found_skills

# ---------------------------
# DB helper function
# ---------------------------
def get_jobs_from_db():
    db = SessionLocal()
    jobs = db.query(Job).all()
    db.close()

    return [
        {
            "role": job.role,
            "skills": job.skills
        }
        for job in jobs
    ]

# ---------------------------
# Home API
# ---------------------------
@app.get("/")
def home():
    return {
        "project": "CareerShield AI",
        "message": "Workforce Intelligence for the AI Era"
    }

# ---------------------------
# Upload Resume API
# ---------------------------
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

# ---------------------------
# Request model
# ---------------------------
class SkillRequest(BaseModel):
    skills: list[str]

class ATSRequest(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]
class ResumeReviewRequest(BaseModel):
    resume_skills: list[str]
    job_skills: list[str]
class CareerRequest(BaseModel):
    skills: list[str]
class LearningTrackerRequest(BaseModel):
    current_skills: list[str]
    target_role: str
# ---------------------------
# Match Job API (SQL + AI)
# ---------------------------
@app.post("/match-job")
async def match_job(data: SkillRequest):

    resume_skills = data.skills

    results = []

    jobs = get_jobs_from_db()

    for job in jobs:
        score, matched, missing = calculate_match(
            resume_skills,
            job["skills"]
        )

        results.append({
            "role": job["role"],
            "match_score": score,
            "matched_skills": matched,
            "missing_skills": missing
        })

    results = sorted(results, key=lambda x: x["match_score"], reverse=True)
    best = results[0]


    missing_skills = best["missing_skills"]

    ROADMAPS = {
        "DBMS": [
            "Week 1: Learn DBMS Fundamentals",
            "Week 2: SQL Queries and Joins",
            "Week 3: Normalization and Indexing",
            "Week 4: Build a Database Mini Project"
        ],
        "React": [
            "Week 1: React Basics",
            "Week 2: Components and Props",
            "Week 3: State Management",
            "Week 4: Build a React Project"
        ],
        "Python": [
            "Week 1: Python Fundamentals",
            "Week 2: Functions and OOP",
            "Week 3: File Handling and APIs",
            "Week 4: Build a Python Project"
        ]
    }

    learning_roadmap = {}

    for skill in missing_skills:
        if skill in ROADMAPS:
            learning_roadmap[skill] = ROADMAPS[skill]

    if best["match_score"] >= 80:
        level = "Strong Profile 🚀"
    elif best["match_score"] >= 50:
        level = "Moderate Profile ⚡"
    else:
        level = "Beginner Profile 📚"

    return {
        "best_match": best,
        "profile_level": level,
        "recommendation": f"Focus on: {', '.join(missing_skills) if missing_skills else 'No major gaps'}",
        "learning_roadmap": learning_roadmap,
        "all_matches": results
    }

# ---------------------------
# Dashboard API
# ---------------------------

@app.get("/dashboard")
def dashboard():

    jobs = get_jobs_from_db()

    skill_count = {}

    for job in jobs:
        for skill in job["skills"]:

            if skill not in skill_count:
                skill_count[skill] = 0

            skill_count[skill] += 1
            most_demanded_skill = max(skill_count, key=skill_count.get)

    career_insight = (
    f"{most_demanded_skill} is currently the most demanded skill "
    f"across available jobs in CareerShield AI."
)

    return {
    "total_jobs": len(jobs),

    "roles": [job["role"] for job in jobs],

    "most_demanded_skill": most_demanded_skill,

    "career_insight": career_insight,

    "skill_frequency": skill_count
}


@app.post("/ats-score")
async def ats_score(data: ATSRequest):

    result = calculate_ats_score(
        data.resume_skills,
        data.job_skills
    )

    return result
# ---------------------------
# Resume Review API
# ---------------------------

@app.post("/resume-review")
async def resume_review(data: ResumeReviewRequest):

    result = review_resume(
        data.resume_skills,
        data.job_skills
    )

    return result

# ---------------------------
# Career Recommender API
# ---------------------------

@app.post("/career-recommendation")
async def career_recommendation(data: CareerRequest):

    result = recommend_careers(data.skills)

    return result

# ---------------------------
# Learning Tracker API
# ---------------------------

@app.post("/learning-tracker")
async def learning_tracker_api(
    data: LearningTrackerRequest
):

    result = learning_tracker(
        data.current_skills,
        data.target_role
    )

    return result