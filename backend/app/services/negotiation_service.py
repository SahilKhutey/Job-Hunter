from typing import Dict, Any, List
from app.core.llm_client import llm_client

class NegotiationService:
    def generate_strategy(self, offer: Dict[str, Any], job_details: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
        """Generates a negotiation strategy and counter-offer script."""
        
        prompt = f"""
        Analyze the following job offer and provide a negotiation strategy.
        
        USER PROFILE:
        {profile.get('summary', 'Senior Engineer')}
        Skills: {', '.join(profile.get('skills', []))}
        
        JOB DETAILS:
        Title: {job_details.get('title')}
        Company: {job_details.get('company')}
        
        CURRENT OFFER:
        Base Salary: {offer.get('base_salary')}
        Equity: {offer.get('equity')}
        Bonus: {offer.get('bonus')}
        
        Return a JSON object with:
        - "offer_grade": 0-100 score
        - "leverage_points": List of 3 key reasons why user deserves more
        - "strategy": A 1-sentence strategic focus
        - "counter_script": A professional email template
        """
        
        # For demo, returning structured mock based on prompt intent
        # In production, call llm_client.complete(prompt)
        
        return {
            "offer_grade": 75,
            "leverage_points": [
                f"Your deep expertise in {profile.get('skills', ['Python'])[0]} is rare for this industry.",
                "The current equity offer is below the 50th percentile for early-stage startups.",
                "You have a track record of leading teams through successful product launches."
            ],
            "strategy": "Focus on increasing the equity stake by 20% and requesting a sign-on bonus to bridge the cash gap.",
            "counter_script": f"Dear Hiring Manager,\n\nThank you so much for the offer for the {job_details.get('title')} role. I am extremely excited about the prospect of joining {job_details.get('company')}.\n\nAfter reviewing the details, I'd like to discuss the compensation package. Given my background in {', '.join(profile.get('skills', [])[:2])}, I was hoping for a total compensation closer to..."
        }

negotiation_service = NegotiationService()
