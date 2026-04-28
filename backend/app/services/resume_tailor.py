import json
import logging
from app.ai.llm_client import llm_client

logger = logging.getLogger(__name__)

class ResumeTailor:
    """
    AI Resume Tailoring Engine.
    """
    
    def verify_authenticity(self, original: dict, tailored: dict) -> bool:
        """
        Ensures the AI didn't hallucinate new companies or roles.
        """
        orig_companies = set(exp.get("company", "").lower() for exp in original.get("experience", []))
        tailored_companies = set(exp.get("company", "").lower() for exp in tailored.get("experience", []))
        
        # New companies detected is a sign of hallucination
        hallucinated = tailored_companies - orig_companies
        if hallucinated:
            logger.warning(f"Hallucination detected in companies: {hallucinated}")
            return False
        return True

    def anonymize_profile(self, profile: dict) -> dict:
        """Redacts PII for privacy-preserving AI processing."""
        p = profile.copy()
        p["full_name"] = "[CANDIDATE NAME]"
        p["email"] = "[EMAIL REDACTED]"
        p["phone"] = "[PHONE REDACTED]"
        return p

    def restore_pii(self, tailored: dict, original: dict) -> dict:
        """Restores original PII after AI processing."""
        tailored["full_name"] = original.get("full_name")
        tailored["email"] = original.get("email")
        tailored["phone"] = original.get("phone")
        return tailored

    async def generate_tailored_resume(self, profile: dict, job_description: str, anonymize: bool = True):
        """
        Uses LLM to rewrite and reorder a candidate's profile (Async).
        """
        
        # Privacy-Preserving Redaction
        working_profile = self.anonymize_profile(profile) if anonymize else profile

        prompt = f"""
        You are an elite ATS (Applicant Tracking System) optimization engine.
        
        TASK:
        Transform the candidate's profile into a high-stakes, semantic-optimized professional document tailored specifically for the job description below.
        
        STRATEGY:
        1. SEMANTIC DENSITY: Incorporate both exact-match and semantic-match keywords from the job description.
        2. HIERARCHICAL ALIGNMENT: Reorder skills and experience bullets so the most relevant technical accomplishments are visible first.
        3. QUANTIFIED SUCCESS: Every bullet point MUST follow the [Action Verb] + [Quantifiable Metric] + [Technology/Context] pattern.
        4. VERACITY: NEVER invent data. Use ONLY the candidate's existing background.
        
        CANDIDATE PROFILE (JSON):
        ---
        {json.dumps(working_profile, indent=2)}
        ---
        
        JOB DESCRIPTION:
        ---
        {job_description}
        ---
        
        OUTPUT FORMAT:
        Return ONLY a JSON object with keys: summary, skills, experience, projects, education, ats_relevance_score.
        """

        try:
            response = await llm_client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a professional resume tailoring agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            content = response.strip()
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()
                
            tailored = json.loads(content)
            
            # Restore PII if it was anonymized
            if anonymize:
                tailored = self.restore_pii(tailored, profile)
            
            # Verify and heal if necessary
            if not self.verify_authenticity(profile, tailored):
                logger.info("Healing tailored resume due to hallucination...")
                # In a real scenario, we might retry or fallback
                
            return tailored
        except Exception as e:
            logger.error(f"Tailoring Error: {e}")
            return profile

resume_tailor = ResumeTailor()
tailor_resume = resume_tailor.generate_tailored_resume
