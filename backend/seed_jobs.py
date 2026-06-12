from backend.database import SessionLocal, Job, Base, engine

Base.metadata.create_all(bind=engine)

db = SessionLocal()

jobs = [
    Job(role="Backend Developer", skills=["Java", "Spring Boot", "SQL", "REST API", "DBMS", "Git"]),
    Job(role="Frontend Developer", skills=["HTML", "CSS", "JavaScript", "React"]),
    Job(role="Full Stack Developer", skills=["Java", "Spring Boot", "React", "SQL", "REST API", "Git"]),
    Job(role="Data Analyst", skills=["SQL", "Python", "Excel", "Statistics", "Power BI"])
]

db.add_all(jobs)
db.commit()
db.close()

print("Jobs inserted into database")