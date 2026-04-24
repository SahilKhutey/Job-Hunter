import re

def extract_keywords(job_description: str):
    """
    Extracts potential keywords from a job description by filtering out common stop words.
    """
    # Simple regex to find words (3+ characters)
    words = re.findall(r'\b[A-Za-z]{3,}\b', job_description.lower())

    # Stop words to filter
    STOP_WORDS = {
        "the", "and", "with", "for", "you", "this", "that", "from", "they", "will",
        "about", "their", "what", "which", "when", "where", "into", "some", "your",
        "over", "only", "other", "than", "then", "also", "most", "some", "such",
        "more", "even", "back", "just", "very", "much", "well", "down", "through"
    }
    
    keywords = [w for w in words if w not in STOP_WORDS]
    
    # Return unique keywords sorted by length (as a simple heuristic for importance)
    return sorted(list(set(keywords)), key=len, reverse=True)
