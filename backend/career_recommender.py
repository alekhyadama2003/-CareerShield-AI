def recommend_careers(skills):

    skills_lower = [skill.lower() for skill in skills]

    recommendations = []

    if (
        "java" in skills_lower and
        "spring boot" in skills_lower and
        "sql" in skills_lower
    ):
        recommendations.append("Backend Developer")

    if (
        "java" in skills_lower and
        "react" in skills_lower
    ):
        recommendations.append("Full Stack Developer")

    if (
        "python" in skills_lower and
        "statistics" in skills_lower
    ):
        recommendations.append("Data Analyst")

    if not recommendations:
        recommendations.append("General Software Engineer")

    return {
        "recommended_roles": recommendations
    }
