print("Recommender started")
certifications = [
    {
        "name": "Machine Learning Foundations",
        "domain": "AI/ML",
        "skills": ["Python", "Statistics"],
        "level": "Beginner"
    },
    {
        "name": "Deep Learning Specialization",
        "domain": "AI/ML",
        "skills": ["Python", "Neural Networks"],
        "level": "Advanced"
    },
    {
        "name": "App Development",
        "domain": "app dev",
        "skills": ["swift","kotlin","flutter"],
        "level": "Intermediate"
    }

]
user = {
    "domain": "AI/ML",
    "skills": ["Python"],
    "level": "Beginner"
}
for cert in certifications:
    matched_skills = []

    for skill in user["skills"]:
        if skill in cert["skills"]:
            matched_skills.append(skill)

    skill_score = len(matched_skills)

    print(cert["name"], "→ matched skills:", matched_skills, "| score:", skill_score)
