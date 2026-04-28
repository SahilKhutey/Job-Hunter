from typing import Dict, Any
from app.agents.orchestrator import Orchestrator
from app.agents.pipeline import pipeline
from app.agents.state import AgentState
import uuid

async def run_application_pipeline(profile: Dict[str, Any], job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Entry point for the Multi-Agent Orchestration (Async).
    Initializes state and runs it through the graph.
    """
    # Create a unique session ID for this pipeline run
    session_id = str(uuid.uuid4())
    
    # Initialize persistent state
    state = AgentState(session_id=session_id, initial_data={
        "profile": profile,
        "job": job,
        "match_score": 0.0,
        "action_decision": "PENDING"
    })
    
    # Initialize the engine
    # pipeline is now List[List[BaseAgent]]
    orchestrator = Orchestrator(pipeline)
    
    # Run the graph (Await)
    final_state = await orchestrator.run(state)
    
    return dict(final_state) # Return as normal dict
