import logging
import asyncio
from typing import Dict, Any
from app.agents.execution_agent import ExecutionAgent
from app.ai.llm_client import llm_client
from app.utils.audit_logger import audit_logger
from app.api.routes.websocket import emit_agent_update, emit_automation_step
from app.models.job import Application
from sqlalchemy.orm import Session
from app.services.automation_service import automation_service
from app.utils.privacy import privacy_shield



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

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # This is a placeholder for the pipeline orchestrator
        # In a real run, this would trigger the async apply()
        logger.info(f"[Agent: {self.name}] Application logic would execute here.")
        return state

    async def apply(self, job_id: int, job_url: str, tailored_resume_path: str):
        """
        Main loop for applying to a job. Handles multi-page forms.
        """
        try:
            audit_logger.log_event("APPLICATION_START", self.user_id, {
                "job_id": job_id,
                "job_url": job_url
            })
            # Detect Platform
            platform = "generic"
            if "linkedin.com" in job_url: platform = "linkedin"
            elif "indeed.com" in job_url: platform = "indeed"
            elif "greenhouse.io" in job_url: platform = "greenhouse"
            elif "lever.co" in job_url: platform = "lever"
            
            await self.browser.start(headless=False, platform=platform)
            
            await emit_automation_step("Navigating", "in_progress")
            await self.browser.navigate(job_url)
            await emit_automation_step("Navigating", "completed")
            
            max_steps = 10
            step_count = 0
            is_complete = False
            
            while step_count < max_steps:
                step_count += 1
                logger.info(f"Processing step {step_count}...")
                
                # Check for success
                if await self._is_success_page():
                    await emit_agent_update("ExecutionAgent", "success", "Success page detected!")
                    is_complete = True
                    break
                
                # 1. Capture Page State
                await emit_agent_update("VisionAgent", "running", f"Analyzing page (Step {step_count})...")
                screenshot_path = await self.browser.screenshot(f"step_{step_count}")
                
                # 2. Extract Elements
                page_content = await self.browser.page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('input, select, textarea, button, [role="button"]')).map(el => {
                        return {
                            tag: el.tagName,
                            type: el.type || el.getAttribute('role'),
                            name: el.name || el.getAttribute('aria-label'),
                            id: el.id,
                            placeholder: el.placeholder,
                            label: el.labels?.[0]?.innerText || el.innerText || '',
                            value: el.value,
                            isVisible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length)
                        }
                    }).filter(e => e.isVisible)
                }""")
                
                # 3. Smart Fill / Action
                await emit_automation_step(f"Step {step_count}: Form Analysis", "in_progress")
                actions_taken = await self._smart_fill_page(page_content)
                await emit_automation_step(f"Step {step_count}: Form Filling", "completed")
                
                # 4. Handle Resume Upload (If on this page)
                if step_count == 1: # Usually on first or last page
                    await self._handle_resume_upload(tailored_resume_path)
                
                # 5. Wait for transition
                await self.browser.wait_for_page_stable()
                
                if not actions_taken:
                    logger.warning("No actions taken on this page. Might be stuck or finished.")
                    break
                
                # 6. HITL if it looks like a final 'Submit'
                # (Heuristic: LLM will mark the action reason as "submit")
                # We handle this inside _smart_fill_page or check here
                
            if is_complete:
                await emit_agent_update("ExecutionAgent", "success", "Application submitted successfully!")
                await self.browser.save_session()
            else:
                await emit_agent_update("ExecutionAgent", "completed", "Application process finished.")
            
            logger.info(f"Successfully processed {job_url}")
            
            # Log to Database
            new_app = Application(
                user_id=int(self.user_id),
                job_id=job_id,
                status="applied" if is_complete else "processed",
                resume_path=tailored_resume_path,
                resume_version="tailored_ai_v1",
                platform=platform,
                application_metadata={"steps_taken": step_count, "final_url": self.browser.page.url}
            )
            self.db.add(new_app)
            self.db.commit()
            
            return True

            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            await emit_agent_update("ExecutionAgent", "error", f"Failed: {str(e)}")
            logger.error(f"Application failed: {e}\n{error_msg}")
            return False
        finally:
            await self.browser.stop()

    async def _smart_fill_page(self, elements: list) -> bool:
        """
        Uses LLM to map user profile data to the identified page elements.
        Returns True if any action was performed.
        """
        # Tokenize profile to prevent PII leakage to LLM
        clean_profile, pii_mapping = privacy_shield.tokenize_profile(self.profile)
        
        await emit_agent_update("AutomationAgent", "running", f"AI mapping {len(elements)} elements to profile...")
        
        actions = llm_client.map_form_fields(clean_profile, elements)
        logger.info(f"AI suggested {len(actions)} actions.")
        actions_taken = 0
        
        for action in actions:
            logger.debug(f"Action data: {action}")
            selector = action.get("selector")
            act_type = action.get("action")
            value = action.get("value")
            reason = action.get("reason", "No reason provided")
            is_nav = action.get("is_navigation", False)
            
            if not selector or not act_type:
                continue
                
            # HITL logic: If reason implies 'final submit' or is_nav is true and name is Submit
            is_final_submit = "submit" in reason.lower() or "finish" in reason.lower()
            
            if is_final_submit:
                await emit_agent_update("ExecutionAgent", "warning", "Final submission button detected. Awaiting review...")
                await automation_service.request_confirmation(str(self.user_id))
            
            await emit_automation_step(f"Action: {act_type} on {selector}", "in_progress")
            logger.info(f"Executing: {act_type} on {selector} ({reason})")
            
            # Unmask value (restore real PII from tokens)
            real_value = privacy_shield.unmask_value(value, pii_mapping)
            
            try:
                if act_type == "type" and real_value:
                    await self.browser.fill_input(selector, real_value)
                    actions_taken += 1
                elif act_type == "click":
                    await self.browser.click_element(selector)
                    actions_taken += 1
                elif act_type == "select" and real_value:
                    await self.browser.page.select_option(selector, real_value)
                    actions_taken += 1
                
                await emit_automation_step(f"Action: {act_type} on {selector}", "completed")
            except Exception as e:
                logger.error(f"Failed action {act_type} on {selector}: {e}")
                await emit_automation_step(f"Action: {act_type} on {selector}", "error")
        
        return actions_taken > 0

    async def _handle_resume_upload(self, path: str):
        """Scans for and uploads the resume."""
        resume_selectors = [
            "input[type='file'][accept*='pdf']",
            "input[type='file'][name*='resume']",
            "input[type='file'][id*='resume']",
            "input[type='file']"
        ]
        for selector in resume_selectors:
            if await self.browser.page.query_selector(selector):
                await emit_automation_step("Resume Upload", "in_progress")
                await self.browser.upload_file(selector, path)
                await emit_automation_step("Resume Upload", "completed")
                return True
        return False

    async def _is_success_page(self) -> bool:
        """Heuristics to detect if the application is complete."""
        success_keywords = ["thank you", "received", "submitted", "confirmed", "success"]
        url = self.browser.page.url.lower()
        
        if any(k in url for k in ["success", "confirmation", "thank-you"]):
            return True
            
        content = await self.browser.page.content()
        content = content.lower()
        
        # Look for these keywords in visible text, not just HTML source
        # But for now, simple content check
        matches = [k for k in success_keywords if k in content]
        return len(matches) >= 2 # At least 2 keywords to be safe

