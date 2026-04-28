import pytest
from app.services.intelligence_engine import intelligence_engine

def test_normalize_skills():
    skills = ["ML", "docker ", "NEXTJS", "UnknownSkill"]
    normalized = intelligence_engine.normalize_skills(skills)
    
    assert "Machine Learning" in normalized
    assert "Docker" in normalized
    assert "Next.js" in normalized
    assert "UnknownSkill" in normalized
    assert len(normalized) == 4

def test_analyze_seniority():
    assert intelligence_engine.analyze_seniority(1) == "Junior"
    assert intelligence_engine.analyze_seniority(3) == "Mid-Level"
    assert intelligence_engine.analyze_seniority(7) == "Senior"
    assert intelligence_engine.analyze_seniority(12) == "Staff / Principal"

def test_parse_duration():
    assert intelligence_engine.parse_duration("5 years of experience") == "5 years"
    assert intelligence_engine.parse_duration("6 months") == "6 months"
    assert intelligence_engine.parse_duration("none") == "unknown"

@pytest.mark.asyncio
async def test_analyze_job_match(mocker):
    # Mock extract_skills_ai to avoid LLM calls
    mocker.patch("app.services.intelligence_engine.UserIntelligenceEngine.extract_skills_ai", 
                 return_value=["python", "react", "aws"])
    
    job_desc = "Looking for a Python and React developer with AWS experience."
    profile = {"skills": ["Python", "AWS"]}
    
    result = await intelligence_engine.analyze_job_match(job_desc, profile)
    
    assert result["score"] > 0
    assert "python" in [s.lower() for s in result["matched_skills"]]
    assert "react" in [s.lower() for s in result["missing_skills"]]

def test_build_skill_graph():
    profile = {
        "skills": ["Python", "Docker"],
        "experience": [
            {"role": "Backend dev", "description": "Used Python for API development"},
            {"role": "DevOps", "description": "Managed Docker containers"}
        ]
    }
    
    graph = intelligence_engine.build_skill_graph(profile)
    
    assert "Python" in graph
    assert "Backend dev" in graph["Python"]["related_roles"]
    assert "DevOps" in graph["Docker"]["related_roles"]

def test_merge_profiles():
    resume = {"skills": ["ml", "aws"], "experience": []}
    linkedin = {"headline": "AI Engineer"}
    github = [{"name": "project1", "description": "desc1", "language": "Python", "fork": False}]
    
    final = intelligence_engine.merge_profiles(resume, linkedin, github)
    
    assert "Machine Learning" in final["skills"]
    assert "AWS" in final["skills"]
    assert final["linkedin_headline"] == "AI Engineer"
    assert len(final["projects"]) == 1
    assert final["projects"][0]["name"] == "project1"
    assert "skill_graph" in final
