def keyword_score(resume_text: str, keywords: list):
    """
    Calculates a match score based on the presence of keywords in the resume.
    """
    resume_text = resume_text.lower()
    
    if not keywords:
        return 100, [], []

    matched = [k for k in keywords if k in resume_text]
    score = int((len(matched) / len(keywords)) * 100)
    
    missing = list(set(keywords) - set(matched))
    
    return score, matched, missing
