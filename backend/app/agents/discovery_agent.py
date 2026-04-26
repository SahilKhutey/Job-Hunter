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
        query = state.get("search_query", "Senior Software Engineer")
        location = state.get("search_location", "Remote")
        logger.info(f"[Agent: {self.name}] Searching for jobs: {query} in {location}")

        # For demo purposes, we simulate the search or target specific platforms
        # In Phase 3, this would navigate to LinkedIn/Indeed search results
        job_urls = await self._discover_linkedin(query, location)
        
        state["discovered_urls"] = job_urls
        logger.info(f"[Agent: {self.name}] Found {len(job_urls)} potential jobs.")
        
        # Save new jobs to DB if they don't exist
        for url in job_urls:
            existing = self.db.query(Job).filter(Job.url == url).first()
            if not existing:
                new_job = Job(
                    title="Discovered Job",
                    company="TBD",
                    url=url,
                    source="LinkedIn",
                    ai_decision="PENDING"
                )
                self.db.add(new_job)
        
        self.db.commit()
        return state

    async def _discover_linkedin(self, query: str, location: str) -> List[str]:
        """Automated search on LinkedIn."""
        try:
            await self.browser.start(headless=True, platform="linkedin")
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={query.replace(' ', '%20')}&location={location}"
            await self.browser.navigate(search_url)
            
            # Extract URLs of job postings
            urls = await self.browser.page.evaluate("""() => {
                const links = Array.from(document.querySelectorAll('a.base-card__full-link'));
                return links.map(a => a.href.split('?')[0]).slice(0, 5); // Limit for demo
            }""")
            
            return urls
        except Exception as e:
            logger.error(f"Discovery failed: {e}")
            return []
        finally:
            await self.browser.stop()
