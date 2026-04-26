import logging
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Graph-Based Execution Engine.
    Passes state between agents sequentially and handles conditional routing.
    """
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("Starting Multi-Agent Orchestration Pipeline...")
        
        for agent in self.agents:
            # Conditional flow logic
            if agent.name in ["resume", "application", "execution"]:
                score = state.get("match_score", 0.0)
                if score < 0.65:
                    logger.info(f"Skipping {agent.name} due to low match score ({score}).")
                    continue
                    
            try:
                state = await agent.run(state)
            except Exception as e:
                logger.error(f"Agent {agent.name} failed: {e}")
                state["error"] = str(e)
                break # Halt pipeline on critical agent failure
                
        logger.info("Multi-Agent Orchestration Pipeline Completed.")
        return state
