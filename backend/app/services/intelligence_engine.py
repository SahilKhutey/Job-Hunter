import re
import httpx
import asyncio
from typing import Dict, Any, List

class UserIntelligenceEngine:
    @staticmethod
    def normalize_skills(skills: List[str]) -> List[str]:
        """Normalizes extracted skills to standard names."""
        if not skills:
            return []
            
        skill_map = {
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence",
            "aws": "AWS",
            "azure": "Azure",
            "docker": "Docker",
            "container": "Docker",
            "graphql": "GraphQL",
            "rest": "REST API",
            "nosql": "NoSQL",
            "sql": "SQL",
            "postgres": "PostgreSQL",
            "postgre": "PostgreSQL",
            "tailwind": "Tailwind CSS",
            "next": "Next.js",
            "nextjs": "Next.js"
        }
        
        normalized = []
        for s in skills:
            if not isinstance(s, str):
                continue
            s_lower = s.strip().lower()
            normalized.append(skill_map.get(s_lower, s.strip()))
            
        return list(set(normalized))

    @staticmethod
    def analyze_seniority(years: int) -> str:
        """Determines seniority based on experience years."""
        if years < 2: return "Junior"
        if years < 5: return "Mid-Level"
        if years < 10: return "Senior"
        return "Staff / Principal"

    @staticmethod
    def parse_duration(text: str) -> str:
        """Extracts experience duration from text."""
        if not text:
            return "unknown"
            
        match = re.search(r'(\d+)\s+(year|month|yr|mo)s?', text.lower())
        return match.group(0) if match else "unknown"

    @staticmethod
    async def extract_skills_ai(text: str) -> List[str]:
        """Uses LLM to extract technical skills from text (Async)."""
        from app.ai.llm_client import llm_client
        prompt = f"Extract only technical skills, languages, and frameworks from this text as a JSON list of strings: {text[:2000]}"
        try:
            skills = await llm_client.generate_structured_json(prompt)
            return UserIntelligenceEngine.normalize_skills(skills)
        except Exception:
            # Fallback to simple extraction
            keywords = ["python", "react", "docker", "aws", "fastapi", "typescript", "kubernetes", "postgres", "sql", "graphql"]
            return [k for k in keywords if k in text.lower()]

    @staticmethod
    def analyze_red_flags(job_description: str) -> dict:
        """Analyzes text for common job post red flags and returns a quantified risk report."""
        flags = []
        indicators = {
            "Burnout Culture": ["unlimited overtime", "hustle culture", "24/7", "work hard play hard", "fast-paced", "rockstar", "ninja", "guru"],
            "Expectation Ambiguity": ["wear many hats", "other duties as assigned", "startup grind", "dynamic environment", "flexible scope"],
            "Compensation Ambiguity": ["competitive salary", "competitive pay", "competitive compensation", "DOE", "negotiable"],
            "Organizational Instability": ["immediate hire", "filling vacancy", "backfill", "urgent", "rapid expansion"]
        }
        
        desc_lower = job_description.lower()
        for flag, keywords in indicators.items():
            if any(k in desc_lower for k in keywords):
                flags.append(flag)
        
        return {
            "flags": flags,
            "risk_score": len(flags) * 25
        }

    @staticmethod
    async def analyze_job_match(job_description: str, profile_data: dict) -> dict:
        """Analyze job description and profile with AI-powered skill extraction and risk analysis (Async)."""
        job_skills = await UserIntelligenceEngine.extract_skills_ai(job_description)
        user_skills = set(profile_data.get("skills", []))
        user_skills_lower = {s.lower() for s in user_skills}
        
        matched = [s for s in job_skills if s.lower() in user_skills_lower]
        missing = [s for s in job_skills if s.lower() not in user_skills_lower]
        
        score = len(matched) / len(job_skills) if job_skills else 0
        
        red_flag_report = UserIntelligenceEngine.analyze_red_flags(job_description)
        
        upskill_advice = ""
        if missing:
            upskill_advice = f"Focus on gaining experience with {missing[0]}. It's a critical requirement for this role."

        return {
            "score": round(score, 2),
            "matched_skills": matched,
            "missing_skills": missing,
            "upskill_advice": upskill_advice,
            "red_flags": red_flag_report["flags"],
            "strategic_risk_score": red_flag_report["risk_score"],
            "seniority_match": True
        }

    @staticmethod
    def build_skill_graph(profile: Dict[str, Any]) -> Dict[str, Any]:
        """Builds a relation graph between skills and experience."""
        graph = {}
        skills = profile.get("skills", [])
        experiences = profile.get("experience", [])
        
        for skill in skills:
            graph[skill] = {"related_roles": []}

        for exp in experiences:
            description = exp.get("description", "").lower()
            role = exp.get("role", "Unknown Role")
            for skill in skills:
                if skill.lower() in description:
                    if role not in graph[skill]["related_roles"]:
                        graph[skill]["related_roles"].append(role)
        return graph

    @staticmethod
    async def fetch_github(username: str) -> List[Dict[str, str]]:
        """Fetches public repositories from GitHub (Async)."""
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.github.com/users/{username}/repos?sort=updated"
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                repos = response.json()
                
                return [
                    {
                        "name": r.get("name"),
                        "description": r.get("description"),
                        "language": r.get("language")
                    }
                    for r in repos if r.get("language") and not r.get("fork")
                ][:10]
            except Exception as e:
                print(f"Error fetching GitHub data for {username}: {e}")
                return []

    @staticmethod
    def extract_linkedin_profile(page) -> Dict[str, str]:
        """Extracts basic info from LinkedIn (Note: Page interaction is already async)."""
        # This is typically called from an async context with a playwright page
        return {} # Placeholder as extraction logic depends on the specific page state

    @staticmethod
    def merge_profiles(resume_data: Dict[str, Any], linkedin_data: Dict[str, Any] = None, github_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Merges intelligence from multiple sources."""
        final = resume_data.copy()
        
        if "skills" in final:
            final["skills"] = UserIntelligenceEngine.normalize_skills(final["skills"])
            
        if linkedin_data:
            if linkedin_data.get("headline"):
                final["linkedin_headline"] = linkedin_data.get("headline")
            
        if github_data:
            if "projects" not in final or not isinstance(final["projects"], list):
                final["projects"] = []
                
            existing_project_names = [p.get("name", "").lower() for p in final["projects"] if isinstance(p, dict)]
            
            for gh_proj in github_data:
                if gh_proj["name"].lower() not in existing_project_names:
                    final["projects"].append({
                        "name": gh_proj["name"],
                        "description": gh_proj["description"],
                        "tech": [gh_proj["language"]] if gh_proj["language"] else []
                    })
                    
        final["skill_graph"] = UserIntelligenceEngine.build_skill_graph(final)
        return final

intelligence_engine = UserIntelligenceEngine()
