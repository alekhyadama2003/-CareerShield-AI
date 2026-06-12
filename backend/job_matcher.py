from sentence_transformers import SentenceTransformer, util

# load AI model once
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_match(user_skills, job_skills):

    # convert lists → sentences
    user_text = " ".join(user_skills)
    job_text = " ".join(job_skills)

    # AI embeddings
    user_vec = model.encode(user_text, convert_to_tensor=True)
    job_vec = model.encode(job_text, convert_to_tensor=True)

    # similarity score (REAL AI)
    score = util.pytorch_cos_sim(user_vec, job_vec).item() * 100

    # AI-based matching (semantic overlap)
    matched = []
    missing = []

    for skill in job_skills:
        if skill.lower() in user_text.lower():
            matched.append(skill)
        else:
            missing.append(skill)

    return round(score, 2), matched, missing