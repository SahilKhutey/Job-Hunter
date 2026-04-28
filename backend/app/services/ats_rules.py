import re

def ats_rules_check(resume_json: dict):
    """
    Performs rule-based checks on the resume structure to identify common ATS parsing issues.
    """
    issues = []
    score = 100

    # 1. Skills Check
    skills = resume_json.get("skills", [])
    if len(skills) < 8:
        issues.append("Low skill density: Consider adding more technical skills and tools.")
        score -= 15
    elif len(skills) > 40:
        issues.append("Skill clutter: Too many skills may dilute your profile's focus.")
        score -= 5

    # 2. Experience Check
    experience = resume_json.get("experience", [])
    if not experience:
        issues.append("Missing Experience: The experience section is critical for ATS evaluation.")
        score -= 40
    else:
        for exp in experience:
            desc = exp.get("description", "")
            # Check for quantified achievements
            if not any(char.isdigit() for char in desc):
                issues.append(f"Non-quantified achievements: Role '{exp.get('role')}' lacks measurable impact (numbers, %, $).")
                score -= 5
            
            # Check for role description length
            if len(desc) < 150:
                issues.append(f"Sparse role description: '{exp.get('role')}' needs more detailed achievements.")
                score -= 10

    # 3. Summary Check
    summary = resume_json.get("summary", "")
    if len(summary) < 150:
        issues.append("Weak Professional Summary: Needs more impact and keywords.")
        score -= 10
    elif len(summary) > 700:
        issues.append("Overly long Summary: Keep it concise for recruiter readability.")
        score -= 5

    # 4. Contact Info Check
    if not resume_json.get("email"):
        issues.append("Missing Email: Crucial for contact.")
        score -= 20
    if not resume_json.get("phone"):
        issues.append("Missing Phone: Required for screening calls.")
        score -= 10
    
    # 5. Education Check
    education = resume_json.get("education", [])
    if not education:
        issues.append("Missing Education: Standard requirement for most ATS filters.")
        score -= 15

    # 6. Links Check
    links = resume_json.get("links", {})
    if not links or not (links.get("linkedin") or links.get("github")):
        issues.append("Missing Social Links: Add LinkedIn or GitHub for professional verification.")
        score -= 5

    return max(0, score), issues
