import json
import logging
from app.services.resume_scorer import score_resume
from app.services.resume_fixer import fix_resume_ai
from app.services.resume_diff import generate_resume_diff

logger = logging.getLogger(__name__)

def auto_fix_resume_pipeline(resume_text: str, resume_json: dict, job_desc: str):
    """
    Orchestrates the 'Score -> Fix -> Re-score -> Diff' pipeline.
    """
    try:
        # 1. Initial Assessment
        original_assessment = score_resume(resume_text, resume_json, job_desc)
        
        # 2. Execute Improvements
        fixed_json = fix_resume_ai(
            resume_json, 
            job_desc, 
            original_assessment["missing_keywords"], 
            original_assessment["structural_issues"]
        )
        
        # 3. Verify Improvements (Re-score)
        # Note: We convert JSON to string for the scorer which expects raw text for some checks
        fixed_text = json.dumps(fixed_json, indent=2)
        new_assessment = score_resume(fixed_text, fixed_json, job_desc)
        
        # 4. Generate Change Log
        changes = generate_resume_diff(resume_json, fixed_json)
        
        return {
            "before": {
                "score": original_assessment["final_score"],
                "keyword_score": original_assessment["keyword_score"],
                "semantic_score": original_assessment["semantic_score"],
                "missing_count": len(original_assessment["missing_keywords"])
            },
            "after": {
                "score": new_assessment["final_score"],
                "keyword_score": new_assessment["keyword_score"],
                "semantic_score": new_assessment["semantic_score"],
                "missing_count": len(new_assessment["missing_keywords"])
            },
            "improvement_delta": new_assessment["final_score"] - original_assessment["final_score"],
            "change_log": changes,
            "optimized_resume": fixed_json
        }
    except Exception as e:
        logger.error(f"Fix Pipeline Error: {e}")
        raise e
