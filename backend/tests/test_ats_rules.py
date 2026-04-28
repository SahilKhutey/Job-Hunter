import pytest
from app.services.ats_rules import ats_rules_check

def test_ats_rules_perfect_resume():
    resume = {
        "summary": "Experienced Software Engineer with 10+ years of expertise in building scalable cloud-native applications. Proven track record of optimizing system performance by 50% and leading cross-functional teams to deliver high-impact projects on time and within budget. Passionate about AI and automation.",
        "skills": ["Python", "AWS", "Docker", "FastAPI", "React", "Next.js", "SQL", "CI/CD", "Kubernetes", "Terraform"],
        "experience": [
            {
                "role": "Senior Developer",
                "description": "Led a team of 5 engineers to design and implement a distributed cloud platform using AWS and Python. Successfully migrated legacy systems to microservices, resulting in a 40% reduction in operational costs and increasing annual revenue by $2M through improved reliability."
            }
        ],
        "email": "test@example.com",
        "phone": "1234567890",
        "education": [{"degree": "B.S. Computer Science"}],
        "links": {"linkedin": "https://linkedin.com/in/test"}
    }
    
    score, issues = ats_rules_check(resume)
    assert score >= 90
    assert len(issues) == 0

def test_ats_rules_missing_info():
    resume = {
        "summary": "Short summary",
        "skills": [],
        "experience": [],
        "education": []
    }
    
    score, issues = ats_rules_check(resume)
    assert score < 50
    assert any("Missing Experience" in i for i in issues)
    assert any("Missing Email" in i for i in issues)

def test_ats_rules_non_quantified():
    resume = {
        "summary": "Long enough summary to pass the summary check. It needs to be over 150 characters long to avoid the weak professional summary issue. So I am writing more text here to reach the threshold. This should be enough now.",
        "skills": ["Python", "AWS", "Docker", "FastAPI", "React", "Next.js", "SQL", "CI/CD"],
        "experience": [
            {
                "role": "Developer",
                "description": "I did some work here but I didn't include any numbers or percentages. This description is also long enough to pass the sparse role description check but it lacks quantified impact."
            }
        ],
        "email": "test@example.com",
        "phone": "1234567890",
        "education": [{"degree": "CS"}],
        "links": {"linkedin": "link"}
    }
    
    score, issues = ats_rules_check(resume)
    assert any("Non-quantified achievements" in i for i in issues)
    # The description is long enough now (over 150 chars), so "Sparse role description" should be gone.
    assert not any("Sparse role description" in i for i in issues)
