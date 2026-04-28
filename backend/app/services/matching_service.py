import numpy as np
import random
import asyncio
from typing import List, Dict, Any, Tuple, Union
from app.services.embedding_service import embedding_service
from app.models.job import Job
from app.models.profile import Profile

class MatchingEngine:
    def __init__(self):
        self.dimension = 384
        try:
            import faiss
            self.index = faiss.IndexFlatL2(self.dimension)
            self.use_mock = False
        except ImportError:
            self.use_mock = True

    async def calculate_metrics(self, profile: Union[Profile, Dict[str, Any]], job: Union[Job, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculates advanced matching metrics (Async). Supports both SQLAlchemy models and raw dictionaries.
        """
        if not profile:
            return {
                "match_score": 0.0,
                "difficulty": 0.5,
                "priority": "MEDIUM",
                "skill_gap": []
            }

        # Handle Dict vs Model access
        def get_val(obj, key, default=None):
            if isinstance(obj, dict):
                val = obj.get(key, default)
            else:
                val = getattr(obj, key, default)
            return val if val is not None else default

        user_skills_raw = get_val(profile, "skills", []) or []
        user_skills = set([s.lower() for s in user_skills_raw if isinstance(s, str)])
        
        job_skills_raw = get_val(job, "skills_required", []) or []
        job_skills = set([s.lower() for s in job_skills_raw if isinstance(s, str)])
        
        # 1. Skill Gap Analysis
        skill_gap = list(job_skills - user_skills)
        intersection = user_skills.intersection(job_skills)
        
        # 2. Base Score Calculation
        skill_match_ratio = len(intersection) / len(job_skills) if job_skills else 0.5
        
        # Get dynamic weights from profile (New Elite Weights)
        weights = get_val(profile, "preference_weights", {}) or {
            "skills": 1.0, "experience": 1.0, "education": 1.0, 
            "location": 1.0, "company_tier": 1.0, "industry_relevance": 1.0
        }
        
        w_skills = weights.get("skills", 1.0)
        w_exp = weights.get("experience", 1.0)
        w_loc = weights.get("location", 1.0)
        w_tier = weights.get("company_tier", 1.0)
        w_rel = weights.get("industry_relevance", 1.0)
        
        # Vector Similarity
        structured = get_val(profile, "structured_data", {}) or {}
        job_title = structured.get("job_title", "")
        summary = get_val(profile, "summary", "") or ""
        
        user_text = f"{job_title}. {summary} {' '.join(user_skills_raw)}"
        
        j_title = get_val(job, "title", "")
        j_desc = get_val(job, "description", "") or ""
        job_text = f"{j_title}. {j_desc[:500]}"
        
        # Use concurrent embedding calls for speed
        u_emb_task = embedding_service.get_embedding(user_text)
        j_emb_task = embedding_service.get_embedding(job_text)
        u_emb, j_emb = await asyncio.gather(u_emb_task, j_emb_task)
        
        # Guard against None or failed embeddings
        if u_emb is None or j_emb is None:
            vector_sim = 0.0
        else:
            norm_u = np.linalg.norm(u_emb)
            norm_j = np.linalg.norm(j_emb)
            if norm_u == 0 or norm_j == 0:
                vector_sim = 0.0
            else:
                vector_sim = float(np.dot(u_emb, j_emb) / (norm_u * norm_j + 1e-9))
        
        # Hybrid Scoring with all weights
        # We'll treat vector_sim as a proxy for 'experience' and 'industry_relevance'
        weighted_score = (
            (vector_sim * w_exp) + 
            (skill_match_ratio * w_skills) +
            (vector_sim * w_rel * 0.5) # Industry relevance boost
        )
        total_weight = w_exp + w_skills + (w_rel * 0.5)
        
        match_score = float(weighted_score / total_weight)
        
        # 3. Risk & Difficulty Score
        risk_score = get_val(job, "strategic_risk_score", 0.0)
        red_flags = get_val(job, "red_flags", []) or []
        
        # Penalize match score if high risk
        risk_penalty = (risk_score / 100.0) * 0.25
        final_match_score = max(0.0, match_score - risk_penalty)
        
        gap_penalty = (len(skill_gap) / len(job_skills)) if job_skills else 0.5
        difficulty = float(gap_penalty * 0.6 + (1.0 - vector_sim) * 0.3 + (risk_score / 100.0) * 0.2)
        
        # Priority Logic: Risk-Aware
        if final_match_score > 0.85 and difficulty < 0.25 and not red_flags and risk_score < 20:
            priority = "HIGH"
        elif final_match_score > 0.65 and len(red_flags) < 2 and risk_score < 50:
            priority = "MEDIUM"
        else:
            priority = "LOW"
            
        return {
            "match_score": round(final_match_score, 2),
            "difficulty": round(difficulty, 2),
            "priority": priority,
            "skill_gap": skill_gap,
            "matched_skills": list(intersection),
            "risk_assessment": {
                "score": risk_score,
                "flags": red_flags,
                "penalty_applied": round(risk_penalty, 3)
            }
        }

    async def match_jobs(self, profile: Profile, jobs: List[Job]) -> List[Tuple[Job, Dict[str, Any]]]:
        if not jobs:
            return []

        # Batch process metrics for high performance
        import asyncio
        tasks = [self.calculate_metrics(profile, job) for job in jobs]
        metrics_list = await asyncio.gather(*tasks)

        results = []
        for i, job in enumerate(jobs):
            results.append((job, metrics_list[i]))

        results.sort(key=lambda x: x[1]["match_score"], reverse=True)
        return results

matching_service = MatchingEngine()
