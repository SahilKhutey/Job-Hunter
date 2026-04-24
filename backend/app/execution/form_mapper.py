from app.ai.llm_client import llm_client

def map_field(label: str, profile: dict) -> str:
    """Smart field mapping logic."""
    if not label:
        return ""
        
    label = label.lower()

    if "name" in label and "first" not in label and "last" not in label:
        return profile.get("full_name", "")
    
    # Handle split names
    if "first name" in label:
        return profile.get("full_name", "").split()[0] if profile.get("full_name") else ""
    if "last name" in label:
        parts = profile.get("full_name", "").split()
        return parts[-1] if len(parts) > 1 else ""

    if "email" in label:
        return profile.get("email", "")

    if "phone" in label:
        return profile.get("phone", "")

    if "linkedin" in label:
        return profile.get("linkedin", "")
        
    if "github" in label:
        return profile.get("github", "")

    return ""

def map_field_llm(label: str, profile: dict) -> str:
    """Fallback LLM mapping for complex fields."""
    prompt = f"""
    Map this form field to the best piece of user data.
    If you don't know, return an empty string. Only return the final text to input.

    Field: {label}
    Profile: {profile}
    """
    # Assuming we added a raw completion method, or using existing text call
    try:
        return llm_client._call_text(prompt, "You are an intelligent form filler.", temperature=0.0)
    except:
        return ""
