def generate_ai_feedback(resume_text: str):
    feedback = []
    text = resume_text.lower()

    # Section checks
    if "experience" not in text:
        feedback.append("Add a Work Experience section.")

    if "project" not in text:
        feedback.append("Include at least 2 technical projects.")

    if "education" not in text:
        feedback.append("Add an Education section.")

    if "skills" not in text:
        feedback.append("Include a Skills section.")

    # Keyword strength
    keywords = [
        "python", "sql", "fastapi",
        "machine learning", "docker",
        "api", "react"
    ]

    matched = [k for k in keywords if k in text]

    if len(matched) < 3:
        feedback.append(
            "Resume lacks strong technical keywords (Python, SQL, APIs, ML, etc.)."
        )

    # Bullet-point quality check
    if "-" not in resume_text and "•" not in resume_text:
        feedback.append("Use bullet points to describe achievements.")

    # Length check
    if len(resume_text.split()) < 250:
        feedback.append("Resume content is too short.")

    if not feedback:
        feedback.append("Resume looks strong.")

    return feedback
