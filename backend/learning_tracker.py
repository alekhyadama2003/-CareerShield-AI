def learning_tracker(current_skills, target_role):

    role_requirements = {
        "Backend Developer": [
            "Java",
            "Spring Boot",
            "SQL",
            "Docker",
            "AWS"
        ],
        "Full Stack Developer": [
            "Java",
            "Spring Boot",
            "React",
            "SQL"
        ],
        "Data Analyst": [
            "Python",
            "SQL",
            "Statistics",
            "Power BI"
        ]
    }

    required_skills = role_requirements.get(
        target_role,
        []
    )

    missing_skills = []

    for skill in required_skills:

        if skill.lower() not in [
            s.lower() for s in current_skills
        ]:
            missing_skills.append(skill)

    return {
        "target_role": target_role,
        "current_skills": current_skills,
        "skills_to_learn": missing_skills
    }