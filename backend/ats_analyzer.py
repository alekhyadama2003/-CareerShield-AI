def calculate_ats_score(resume_skills, job_skills):

    matched = []
    missing = []

    for skill in job_skills:

        if skill.lower() in [s.lower() for s in resume_skills]:
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) == 0:
        score = 0
    else:
        score = round((len(matched) / len(job_skills)) * 100, 2)

    if score >= 80:
        strength = "Strong"
        readiness = "High"
    elif score >= 50:
        strength = "Moderate"
        readiness = "Medium"
    else:
        strength = "Weak"
        readiness = "Low"

    suggestions = []

    for skill in missing:

        if skill == "Docker":
            suggestions.append(
                "Learn Docker containers and deploy a sample application"
            )

        elif skill == "AWS":
            suggestions.append(
                "Complete AWS Cloud Practitioner fundamentals"
            )

        elif skill == "React":
            suggestions.append(
                "Build a React project with components and state management"
            )

        else:
            suggestions.append(
                f"Learn {skill} through projects and practice"
            )

    return {
        "ats_score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "resume_strength": strength,
        "interview_readiness": readiness,
        "suggestions": suggestions
    }
