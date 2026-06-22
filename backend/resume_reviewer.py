def review_resume(resume_skills, job_skills):

    missing_keywords = []

    for skill in job_skills:

        if skill.lower() not in [s.lower() for s in resume_skills]:
            missing_keywords.append(skill)

    tips = []

    for skill in missing_keywords:

        if skill == "Docker":
            tips.append(
                "Add a project using Docker containers."
            )

        elif skill == "AWS":
            tips.append(
                "Mention cloud deployment experience."
            )

        elif skill == "React":
            tips.append(
                "Show frontend projects using React."
            )

        else:
            tips.append(
                f"Add evidence of {skill} through projects."
            )

    return {
        "missing_keywords": missing_keywords,
        "resume_tips": tips
    }
