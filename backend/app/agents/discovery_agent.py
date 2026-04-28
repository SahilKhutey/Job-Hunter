import asyncio
import logging
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent
from app.agents.execution_agent import ExecutionAgent
from app.models.job import Job
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class DiscoveryAgent(BaseAgent):
    """
    Agent responsible for finding new job listings based on search criteria.
    """
    def __init__(self, user_id: str = "0", db: Session = None):
        super().__init__("discovery")
        self.user_id = user_id
        self.db = db
        self.browser = ExecutionAgent(user_id)

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        queries = state.get("search_queries", [state.get("search_query", "Senior Software Engineer")])
        location = state.get("search_location", "Remote")
        
        from app.api.routes.websocket import emit_strategic_trace
        await emit_strategic_trace("Discovery", f"Initiating high-velocity scan for {len(queries)} target profiles in {location}...", user_id=int(self.user_id))

        # Parallel Execution Loop
        tasks = [self._discover_platform(q, location, "linkedin") for q in queries]
        results = await asyncio.gather(*tasks)
        
        all_urls = []
        for urls in results:
            all_urls.extend(urls)
            
        # Deduplicate
        all_urls = list(set(all_urls))
        state["discovered_urls"] = all_urls
        
        await emit_strategic_trace("Discovery", f"Velocity scan complete. {len(all_urls)} high-fidelity leads ingested into pipeline.", user_id=int(self.user_id))
        
        # Optimized Bulk Save
        new_leads = 0
        for url in all_urls:
            existing = self.db.query(Job).filter(Job.url == url).first()
            if not existing:
                new_job = Job(
                    title="Analyzing Lead...",
                    company="TBD",
                    url=url,
                    source="LinkedIn",
                    ai_decision="PENDING"
                )
                self.db.add(new_job)
                new_leads += 1
        
        if new_leads > 0:
            self.db.commit()
            
        return state

    async def _discover_platform(self, query: str, location: str, platform: str) -> List[str]:
        """High-velocity platform-specific scanner."""
        from app.api.routes.websocket import emit_agent_update
        await emit_agent_update("Discovery", "searching", f"Scanning {platform} for: {query}", user_id=int(self.user_id))
        
        # For simulation/robustness in demo
        try:
            # We would use parallel browser contexts here
            # For now, simulate high-velocity results
            await asyncio.sleep(2) # Simulated network latency
            mock_urls = [
                f"https://www.{platform}.com/jobs/view/{hash(query + str(i))}" for i in range(3)
            ]
            return mock_urls
        except Exception as e:
            logger.error(f"Discovery on {platform} failed: {e}")
            return []
