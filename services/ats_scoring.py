def calculate_ats_score(resume_text: str):
    score = 0
    feedback = []

    text = resume_text.lower()

    sections = ["education", "skills", "experience", "projects"]

    for section in sections:
        if section in text:
            score += 10
        else:
            feedback.append(f"Missing section: {section}")

    keywords = [
        "python", "sql", "api", "react",
        "machine learning", "docker", "fastapi"
    ]

    matches = 0
    for word in keywords:
        if word in text:
            matches += 1

    score += matches * 5

    if matches < 3:
        feedback.append("Add more technical keywords")

    return {
        "score": min(score, 100),
        "feedback": feedback
    }
