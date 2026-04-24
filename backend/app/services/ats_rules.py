def ats_rules_check(resume_json: dict):
    """
    Performs rule-based checks on the resume structure to identify common ATS parsing issues.
    """
    issues = []
    score = 100

    # Skills Check
    skills = resume_json.get("skills", [])
    if len(skills) < 10:
        issues.append("Low skill density: Consider adding more technical skills and tools.")
        score -= 10
    elif len(skills) > 50:
        issues.append("Skill clutter: Too many skills may dilute your profile's focus.")
        score -= 5

    # Experience Check
    experience = resume_json.get("experience", [])
    if not experience:
        issues.append("Missing Experience: The experience section is critical for ATS evaluation.")
        score -= 30
    else:
        for exp in experience:
            bullets = exp.get("bullets", [])
            if len(bullets) < 3:
                issues.append(f"Sparse role description: '{exp.get('role')}' needs more detailed achievements.")
                score -= 5

    # Summary Check
    summary = resume_json.get("summary", "")
    if len(summary) < 100:
        issues.append("Weak Professional Summary: Needs more impact and keywords.")
        score -= 10
    elif len(summary) > 600:
        issues.append("Overly long Summary: Keep it concise for recruiter readability.")
        score -= 5

    # Contact Info Check
    if not resume_json.get("email"):
        issues.append("Missing Email: Crucial for contact.")
        score -= 10
    if not resume_json.get("phone"):
        issues.append("Missing Phone: Required for screening calls.")
        score -= 5

    return max(0, score), issues
