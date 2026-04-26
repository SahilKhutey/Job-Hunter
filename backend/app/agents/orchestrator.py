import logging
from typing import List, Dict, Any
from app.agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class Orchestrator:
    """
    Advanced Orchestration Engine.
    Supports stages of execution where agents within a stage run in parallel.
    """
    def __init__(self, stages: List[List[BaseAgent]]):
        self.stages = stages # List of stages, each stage is a list of agents

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Starting Advanced Orchestration with {len(self.stages)} stages...")
        
        for i, stage in enumerate(self.stages):
            logger.info(f"--- Stage {i+1} ({len(stage)} agents) ---")
            
            # Parallel execution within the stage
            tasks = []
            for agent in stage:
                # Flow Control: Skip certain agents if state conditions aren't met
                if agent.name in ["resume", "application", "execution"]:
                    score = state.get("match_score", 0.0)
                    if score < 0.65:
                        logger.info(f"Skipping {agent.name} due to low match score ({score}).")
                        continue
                
                tasks.append(self._run_agent(agent, state))
            
            if not tasks:
                continue
                
            # Execute all agents in this stage in parallel
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Merge results back into state
            for res in results:
                if isinstance(res, Exception):
                    logger.error(f"Stage failure: {res}")
                    state["error"] = str(res)
                    continue
                if isinstance(res, dict):
                    state.update(res)
                    
            if state.get("error"):
                logger.warning("Halting orchestration due to errors in previous stage.")
                break
                
        logger.info("Advanced Orchestration Pipeline Completed.")
        return state

    async def _run_agent(self, agent: BaseAgent, state: Dict[str, Any]) -> Dict[str, Any]:
        """Wrapper for single agent execution with logging."""
        logger.info(f"[Agent: {agent.name}] Starting...")
        # Create a local copy of state for the agent to work on if needed, 
        # or just pass it in. For now, simple shared state.
        return await agent.run(state)
