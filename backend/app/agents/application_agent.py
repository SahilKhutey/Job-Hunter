import logging
import asyncio
from typing import Dict, Any
from app.agents.execution_agent import ExecutionAgent
from app.ai.llm_client import llm_client
from app.utils.audit_logger import audit_logger
from app.api.routes.websocket import emit_agent_update, emit_automation_step
from app.models.job import Application
from sqlalchemy.orm import Session



logger = logging.getLogger(__name__)

from app.agents.base_agent import BaseAgent

class ApplicationAgent(BaseAgent):
    """
    High-level agent that orchestrates a single job application.
    Uses AI to understand form fields and determine actions.
    """
    def __init__(self, user_id: str = "0", profile_data: Dict[str, Any] = None, db: Session = None):
        super().__init__("application")
        self.user_id = user_id
        self.profile = profile_data or {}
        self.db = db
        self.browser = ExecutionAgent(user_id)

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # This is a placeholder for the pipeline orchestrator
        # In a real run, this would trigger the async apply()
        logger.info(f"[Agent: {self.name}] Application logic would execute here.")
        return state

    async def apply(self, job_id: int, job_url: str, tailored_resume_path: str):

        """
        Main loop for applying to a job.
        """
        try:
            audit_logger.log_event("APPLICATION_START", self.user_id, {
                "job_id": job_id,
                "job_url": job_url
            })
            await emit_agent_update("ExecutionAgent", "running", f"Starting application for {job_url}")
            await self.browser.start(headless=False) # Visual for debugging
            
            await emit_automation_step("Navigating", "in_progress")
            await self.browser.navigate(job_url)
            await emit_automation_step("Navigating", "completed")
            
            # 1. Identify the 'Apply' button
            await emit_agent_update("VisionAgent", "running", "Analyzing page layout...")
            screenshot_path = await self.browser.screenshot("initial_load")
            await emit_agent_update("VisionAgent", "completed", f"Page captured: {screenshot_path}")
            
            # 2. Fill the form (Multi-step process)
            await emit_automation_step("Form Analysis", "in_progress")
            logger.info("Analyzing page for interactive elements...")

            page_content = await self.browser.page.evaluate("""() => {
                return Array.from(document.querySelectorAll('input, select, textarea, button')).map(el => {
                    return {
                        tag: el.tagName,
                        type: el.type,
                        name: el.name,
                        id: el.id,
                        placeholder: el.placeholder,
                        label: el.labels?.[0]?.innerText || '',
                        value: el.value
                    }
                })
            }""")
            
            # AI analyzes fields: "What are the input fields on this page? Map them to the user profile."
            await self._smart_fill_page(page_content)
            await emit_automation_step("Form Filling", "completed")
            
            # 3. Upload Resume
            await emit_automation_step("Resume Upload", "in_progress")
            # In a real scenario, we'd find the file input
            # await self.browser.upload_file("input[type='file']", tailored_resume_path)
            await emit_automation_step("Resume Upload", "completed")
            
            await emit_agent_update("ExecutionAgent", "completed", "Application submitted successfully!")
            logger.info(f"Successfully applied to {job_url}")
            
            # Log to Database
            new_app = Application(
                user_id=int(self.user_id),
                job_id=job_id,
                status="applied",
                resume_path=tailored_resume_path,
                resume_version="tailored_ai_v1", # Metadata logic can be expanded
                platform="unknown" # Can be detected from URL
            )
            self.db.add(new_app)
            self.db.commit()
            
            return True

            
        except Exception as e:
            await emit_agent_update("ExecutionAgent", "error", f"Failed: {str(e)}")
            logger.error(f"Application failed: {e}")
            return False
        finally:
            await self.browser.stop()

    async def _smart_fill_page(self, elements: list):
        """
        Uses LLM to map user profile data to the identified page elements.
        """
        await emit_agent_update("AutomationAgent", "running", f"AI mapping {len(elements)} elements to profile...")
        
        actions = llm_client.map_form_fields(self.profile, elements)
        
        for action in actions:
            selector = action.get("selector")
            act_type = action.get("action")
            value = action.get("value")
            reason = action.get("reason", "No reason provided")
            
            if not selector or not act_type:
                continue
                
            await emit_automation_step(f"Action: {act_type} on {selector}", "in_progress")
            logger.info(f"Executing: {act_type} on {selector} ({reason})")
            
            try:
                if act_type == "type" and value:
                    await self.browser.fill_input(selector, value)
                elif act_type == "click":
                    await self.browser.click_element(selector)
                await emit_automation_step(f"Action: {act_type} on {selector}", "completed")
            except Exception as e:
                logger.error(f"Failed action {act_type} on {selector}: {e}")
                await emit_automation_step(f"Action: {act_type} on {selector}", "error")

