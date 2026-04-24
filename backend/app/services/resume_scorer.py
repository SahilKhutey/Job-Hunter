import json
from app.services.keyword_extractor import extract_keywords
from app.services.keyword_matcher import keyword_score
from app.services.semantic_match import semantic_score
from app.services.ats_rules import ats_rules_check
from app.services.resume_feedback_ai import generate_resume_feedback

def score_resume(resume_text: str, resume_json: dict, job_desc: str):
    """
    Orchestrates the multi-layered scoring of a resume against a job description.
    """
    # 1. Keyword Extraction & Matching
    keywords = extract_keywords(job_desc)
    kw_score, matched, missing = keyword_score(resume_text, keywords)
    
    # 2. Semantic Similarity
    sem_score = semantic_score(resume_text, job_desc)
    
    # 3. Structural/Rule Checks
    rule_score, issues = ats_rules_check(resume_json)
    
    # 4. Final Weighted Score
    # Keyword: 40%, Semantic: 40%, Rules: 20%
    final_score = int((kw_score * 0.4) + (sem_score * 0.4) + (rule_score * 0.2))
    
    # 5. Qualitative Feedback
    feedback = generate_resume_feedback(resume_text, job_desc, missing)
    
    return {
        "final_score": final_score,
        "keyword_score": kw_score,
        "semantic_score": sem_score,
        "rule_score": rule_score,
        "matched_keywords": matched[:20],
        "missing_keywords": missing[:15],
        "structural_issues": issues,
        "feedback": feedback
    }
