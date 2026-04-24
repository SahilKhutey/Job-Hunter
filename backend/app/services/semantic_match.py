import numpy as np
from app.ai.llm_client import llm_client

def cosine_similarity(a, b):
    """
    Calculates cosine similarity between two vectors.
    """
    if not a or not b:
        return 0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_score(resume_text: str, job_desc: str):
    """
    Calculates a semantic similarity score between resume and job description using embeddings.
    """
    emb_resume = llm_client.get_embedding(resume_text)
    emb_job = llm_client.get_embedding(job_desc)
    
    if not emb_resume or not emb_job:
        return 0
        
    similarity = cosine_similarity(emb_resume, emb_job)
    
    # Scale similarity to 0-100
    # Embedding similarities are usually between 0.6 and 0.9 for relevant text
    # We can normalize it slightly
    score = int(max(0, (similarity - 0.5) / 0.5) * 100) if similarity > 0.5 else int(similarity * 100)
    
    return min(100, score)
