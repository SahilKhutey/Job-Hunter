def generate_resume_diff(old_json: dict, new_json: dict):
    """
    Compares two resume JSON objects and returns a list of high-level changes made.
    """
    changes = []

    # Summary Check
    if old_json.get("summary") != new_json.get("summary"):
        changes.append("Professional summary optimized for impact and keyword alignment.")

    # Skills Check
    old_skills = set(old_json.get("skills", []))
    new_skills = set(new_json.get("skills", []))
    added_skills = list(new_skills - old_skills)
    if added_skills:
        changes.append(f"Injected {len(added_skills)} missing technical keywords into the skills section.")

    # Experience Check
    old_exp = old_json.get("experience", [])
    new_exp = new_json.get("experience", [])
    
    if len(old_exp) == len(new_exp):
        enhanced_count = 0
        for i in range(len(old_exp)):
            if old_exp[i].get("bullets") != new_exp[i].get("bullets"):
                enhanced_count += 1
        if enhanced_count > 0:
            changes.append(f"Enhanced bullet points for {enhanced_count} previous roles with action verbs and metrics.")
    elif len(new_exp) != len(old_exp):
         changes.append("Experience section structure updated.")

    return changes
