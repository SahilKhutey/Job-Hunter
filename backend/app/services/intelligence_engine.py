import re
import requests
from typing import Dict, Any, List

class UserIntelligenceEngine:
    @staticmethod
    def normalize_skills(skills: List[str]) -> List[str]:
        """Normalizes extracted skills to standard names."""
        if not skills:
            return []
            
        skill_map = {
            "py": "Python",
            "reactjs": "React",
            "react.js": "React",
            "node": "Node.js",
            "js": "JavaScript",
            "ts": "TypeScript",
            "aws": "AWS",
            "gcp": "Google Cloud",
            "k8s": "Kubernetes",
            "ml": "Machine Learning",
            "ai": "Artificial Intelligence"
        }
        
        normalized = []
        for s in skills:
            if not isinstance(s, str):
                continue
            s_lower = s.strip().lower()
            normalized.append(skill_map.get(s_lower, s.strip()))
            
        return list(set(normalized))

    @staticmethod
    def parse_duration(text: str) -> str:
        """Extracts experience duration from text."""
        if not text:
            return "unknown"
            
        match = re.search(r'(\d+)\s+(year|month|yr|mo)s?', text.lower())
        return match.group(0) if match else "unknown"

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
    def fetch_github(username: str) -> List[Dict[str, str]]:
        """Fetches public repositories from GitHub."""
        try:
            url = f"https://api.github.com/users/{username}/repos?sort=updated"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            repos = response.json()
            
            return [
                {
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "language": r.get("language")
                }
                for r in repos if r.get("language") and not r.get("fork")
            ][:10] # Take top 10 recent non-forked repos
        except Exception as e:
            print(f"Error fetching GitHub data for {username}: {e}")
            return []

    @staticmethod
    def extract_linkedin_profile(page) -> Dict[str, str]:
        """Extracts basic info from a logged-in LinkedIn session."""
        try:
            name = page.inner_text("h1", timeout=5000)
            headline = page.inner_text(".text-body-medium", timeout=5000)
            return {
                "name": name,
                "headline": headline
            }
        except Exception as e:
            print(f"Error extracting LinkedIn data: {e}")
            return {}

    @staticmethod
    def merge_profiles(resume_data: Dict[str, Any], linkedin_data: Dict[str, Any] = None, github_data: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Merges intelligence from multiple sources."""
        final = resume_data.copy()
        
        # Normalize resume skills
        if "skills" in final:
            final["skills"] = UserIntelligenceEngine.normalize_skills(final["skills"])
            
        if linkedin_data:
            if linkedin_data.get("headline"):
                final["linkedin_headline"] = linkedin_data.get("headline")
            
        if github_data:
            if "projects" not in final or not isinstance(final["projects"], list):
                final["projects"] = []
                
            # Deduplicate by name roughly
            existing_project_names = [p.get("name", "").lower() for p in final["projects"] if isinstance(p, dict)]
            
            for gh_proj in github_data:
                if gh_proj["name"].lower() not in existing_project_names:
                    final["projects"].append({
                        "name": gh_proj["name"],
                        "description": gh_proj["description"],
                        "tech": [gh_proj["language"]] if gh_proj["language"] else []
                    })
                    
        # Generate the graph
        final["skill_graph"] = UserIntelligenceEngine.build_skill_graph(final)
                    
        return final

intelligence_engine = UserIntelligenceEngine()
