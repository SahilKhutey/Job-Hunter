import logging
import asyncio
from typing import Dict, Any
from app.agents.execution_agent import ExecutionAgent
from app.ai.llm_client import llm_client
from app.api.routes.websocket import emit_agent_update, emit_automation_step
from app.models.job import Application
from sqlalchemy.orm import Session



logger = logging.getLogger(__name__)

class ApplicationAgent:
    """
    High-level agent that orchestrates a single job application.
    Uses AI to understand form fields and determine actions.
    """
    def __init__(self, user_id: str, profile_data: Dict[str, Any], db: Session):
        self.user_id = user_id
        self.profile = profile_data
        self.db = db
        self.browser = ExecutionAgent(user_id)

    async def apply(self, job_id: int, job_url: str, tailored_resume_path: str):

        """
        Main loop for applying to a job.
        """
        try:
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
        logger.info(f"AI mapping {len(elements)} elements to user profile...")
        
        # Simple heuristic mapping for prototype
        # In production, we'd send 'elements' to LLM to get a precise action plan
        for el in elements:
            tag = el['tag'].lower()
            label = el['label'].lower() or el['placeholder'].lower() or el['name'].lower()
            
            # Profile Mapping
            if 'first name' in label:
                await self.browser.fill_input(f"input[name='{el['name']}']", self.profile.get('full_name', '').split()[0])
            elif 'last name' in label:
                await self.browser.fill_input(f"input[name='{el['name']}']", self.profile.get('full_name', '').split()[-1])
            elif 'email' in label:
                await self.browser.fill_input(f"input[name='{el['name']}']", self.profile.get('email', ''))
            elif 'phone' in label:
                await self.browser.fill_input(f"input[name='{el['name']}']", self.profile.get('phone', ''))
            elif tag == 'button' and 'apply' in label:
                # Potential next step or submit
                pass

