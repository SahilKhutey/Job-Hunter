from app.agents.profile_agent import ProfileAgent
from app.agents.job_agent import JobAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.resume_agent import ResumeAgent
from app.agents.application_agent import ApplicationAgent
from app.agents.execution_agent import ExecutionAgent
from app.agents.learning_agent import LearningAgent

# Define the standard execution sequence as STAGES
# Each inner list represents agents that can run in PARALLEL within that stage.
pipeline = [
    [ProfileAgent(), JobAgent()], # Stage 1: Prep
    [MatchingAgent()],             # Stage 2: Assessment
    [ResumeAgent()],               # Stage 3: Content Creation
    [ApplicationAgent()],          # Stage 4: Strategic Positioning
    [ExecutionAgent()],            # Stage 5: Deployment
    [LearningAgent()]              # Stage 6: Post-execution analysis
]
