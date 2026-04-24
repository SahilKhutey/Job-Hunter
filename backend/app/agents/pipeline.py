from app.agents.profile_agent import ProfileAgent
from app.agents.job_agent import JobAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.resume_agent import ResumeAgent
from app.agents.application_agent import ApplicationAgent
from app.agents.execution_agent import ExecutionAgent
from app.agents.learning_agent import LearningAgent

# Define the standard execution sequence
pipeline = [
    ProfileAgent(),
    JobAgent(),
    MatchingAgent(),
    ResumeAgent(),
    ApplicationAgent(),
    ExecutionAgent(),
    LearningAgent()
]
