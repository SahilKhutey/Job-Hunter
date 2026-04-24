from typing import Dict, Any, List
from app.ai.llm_client import llm_client

class ContentGenerator:
    """
    Application Content Generation Engine (Cover Letter & Form Answers).
    """
    
    def generate_application_content(self, profile: Dict[str, Any], job: Dict[str, Any], company_text: str = None) -> Dict[str, Any]:
        """Main pipeline for generating cover letters and form answers."""
        
        # 1. Job Understanding
        job_context = llm_client.analyze_job(job.get("description", ""))
        
        # 2. Company Context (Optional)
        company_context = None
        if company_text:
            company_context = llm_client.extract_company_context(company_text)
            
        # Enhance job dict with contexts
        enhanced_job = {**job, "context": job_context, "company_context": company_context}
        
        # 3. User Positioning Engine
        positioning = llm_client.generate_positioning(profile, enhanced_job)
        
        # 4. Cover Letter Generation
        cover_letter = llm_client.generate_cover_letter(profile, enhanced_job, positioning)
        
        # 5. Smart Form Answer Generation
        questions = [
            "Why do you want to work here?",
            "Why are you a good fit?",
            "Describe a challenging project you worked on.",
            "What are your salary expectations?"
        ]
        
        answers = llm_client.generate_form_answers(profile, enhanced_job, questions)
        
        return {
            "cover_letter": cover_letter,
            "answers": answers,
            "positioning": positioning
        }

content_generator = ContentGenerator()
