def calculate_match(resume_skills, job_skills):
    matched = list(set(resume_skills) & set(job_skills))
    missing = list(set(job_skills) - set(resume_skills))

    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100)

    return {
        "match_score": score,
        "matched_skills": matched,
        "missing_skills": missing
    }