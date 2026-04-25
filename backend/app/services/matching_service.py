import numpy as np
import random
from typing import List, Dict, Any, Tuple
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

    def calculate_metrics(self, profile: Profile, job: Job) -> Dict[str, Any]:
        """
        Calculates advanced matching metrics: match_score, difficulty, priority, and skill gap.
        """
        if not profile:
            return {
                "match_score": 0.0,
                "difficulty": 0.5,
                "priority": "MEDIUM",
                "skill_gap": []
            }

        user_skills = set([s.lower() for s in (profile.skills or [])])
        job_skills = set([s.lower() for s in (job.skills_required or [])])
        
        # 1. Skill Gap Analysis
        skill_gap = list(job_skills - user_skills)
        intersection = user_skills.intersection(job_skills)
        
        # 2. Base Score Calculation
        skill_match_ratio = len(intersection) / len(job_skills) if job_skills else 0.5
        
        # Vector Similarity
        job_title = (profile.structured_data or {}).get("job_title", "")
        user_text = f"{job_title}. {profile.summary or ''} {' '.join(profile.skills or [])}"
        job_text = f"{job.title}. {job.description[:500]}"
        
        u_emb = embedding_service.get_embedding(user_text)
        j_emb = embedding_service.get_embedding(job_text)
        
        vector_sim = np.dot(u_emb, j_emb) / (np.linalg.norm(u_emb) * np.linalg.norm(j_emb) + 1e-9)
        
        match_score = float(vector_sim * 0.6 + skill_match_ratio * 0.4)
        
        # 3. Difficulty Score (0.0 to 1.0)
        # Higher gap = Higher difficulty
        gap_penalty = (len(skill_gap) / len(job_skills)) if job_skills else 0.5
        difficulty = float(gap_penalty * 0.7 + (1.0 - vector_sim) * 0.3)
        
        # 4. Apply Priority
        if match_score > 0.8 and difficulty < 0.3:
            priority = "HIGH"
        elif match_score > 0.6:
            priority = "MEDIUM"
        else:
            priority = "LOW"
            
        return {
            "match_score": round(match_score, 2),
            "difficulty": round(difficulty, 2),
            "priority": priority,
            "skill_gap": skill_gap
        }

    def match_jobs(self, profile: Profile, jobs: List[Job]) -> List[Tuple[Job, Dict[str, Any]]]:
        if not jobs:
            return []

        results = []
        for job in jobs:
            metrics = self.calculate_metrics(profile, job)
            results.append((job, metrics))

        results.sort(key=lambda x: x[1]["match_score"], reverse=True)
        return results

matching_service = MatchingEngine()
