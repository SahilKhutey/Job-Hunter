import os
import asyncio
import base64
import logging
import random
from typing import Dict, Any, Optional
from app.api.routes.websocket import emit_agent_update, manager

logger = logging.getLogger(__name__)

class HumanBehavior:
    """Simulates human interaction patterns to evade bot detection."""
    
    @staticmethod
    async def jitter_delay(min_ms: int = 500, max_ms: int = 2000):
        """Adds a randomized delay."""
        delay = random.uniform(min_ms, max_ms) / 1000
        await asyncio.sleep(delay)

    @staticmethod
    async def mouse_jitter(page):
        """Simulates subtle mouse movements."""
        try:
            x = random.randint(0, 500)
            y = random.randint(0, 500)
            await page.mouse.move(x, y, steps=10)
        except Exception:
            pass

    @staticmethod
    async def scroll_behavior(page):
        """Mimics a user scrolling through the job description."""
        try:
            for _ in range(random.randint(2, 4)):
                await page.mouse.wheel(0, random.randint(300, 600))
                await asyncio.sleep(random.uniform(0.5, 1.5))
            # Scroll back up a bit
            await page.mouse.wheel(0, -random.randint(200, 400))
        except Exception:
            pass
class AutomationService:
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.sessions_dir = "sessions"
        self.use_mock = False
        self.confirmation_events: Dict[str, asyncio.Event] = {}
        
        if not os.path.exists(self.sessions_dir):
            os.makedirs(self.sessions_dir)
        
        try:
            import playwright
            from playwright.async_api import async_playwright
            from playwright_stealth import stealth_async
        except ImportError:
            print("Playwright or Stealth not found. Automation features will be mocked.")
            self.use_mock = True

    def _get_session_path(self, platform: str) -> str:
        return os.path.join(self.sessions_dir, f"{platform}_session.json")

    async def log(self, message: str, status: str = "running", agent: str = "Hunter AI", user_id: Optional[int] = None):
        print(f"[{agent}] {message}")
        await emit_agent_update(agent, status, message, user_id=user_id)

    async def request_confirmation(self, job_id: str, user_id: Optional[int] = None):
        """Pauses execution and waits for a WebSocket confirmation from the user."""
        event = asyncio.Event()
        self.confirmation_events[job_id] = event
        await self.log("Awaiting manual confirmation for submission...", "warning", user_id=user_id)
        
        await manager.broadcast({
            "type": "awaiting_confirmation",
            "job_id": job_id,
            "message": "The application is ready. Please review and confirm submission."
        }, user_id=user_id)
        
        await event.wait()
        if job_id in self.confirmation_events:
            del self.confirmation_events[job_id]
        await self.log("Confirmation received. Proceeding with submission.", "success", user_id=user_id)

    async def confirm_application(self, job_id: str):
        """Triggered by the frontend to resume a paused application."""
        if job_id in self.confirmation_events:
            self.confirmation_events[job_id].set()
            return True
        return False

    async def emit_screenshot(self, page=None, user_id: Optional[int] = None):
        """Captures a screenshot and sends it over WS."""
        try:
            if page:
                screenshot = await page.screenshot(type="jpeg", quality=40)
                encoded = base64.b64encode(screenshot).decode('utf-8')
            else:
                # Simulation frame
                encoded = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8ED5GWEZGPDpCUXFiS0VUXHdcemZpfHBsfXxlfHpwfh5uYHSUdH1viJqrj4yVmZ5vboqz0561p5mXm5X/2wBDAQlgREBIUHLiYmLi5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mX/wAARCAABAAEASIAEARED/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gALAwEAAhEDEQA/AL+AD//Z"
            
            await manager.broadcast({
                "type": "browser_view",
                "image": encoded
            }, user_id=user_id)
        except Exception as e:
            print(f"Screenshot failed: {e}")

    async def fill_form(self, page, user_identity: Dict[str, Any], user_id: Optional[int] = None):
        """Intelligently fills application forms with stealth and human-like delays."""
        await self.log("Analyzing application form with Stealth-Vision...", "running", agent="Filling Agent", user_id=user_id)
        await HumanBehavior.mouse_jitter(page)
        
        fields = await page.query_selector_all("input, textarea, select")
        questions = []

        for field in fields:
            try:
                # Visibility check
                if not await field.is_visible(): continue
                
                label_text = ""
                field_id = await field.get_attribute("id")
                if field_id:
                    label = await page.query_selector(f"label[for='{field_id}']")
                    if label:
                        label_text = await label.inner_text()
                
                placeholder = await field.get_attribute("placeholder") or ""
                name_attr = await field.get_attribute("name") or ""
                descriptor = f"{label_text} {placeholder} {name_attr}".strip().lower()
                
                if not descriptor: continue

                # Heuristic filling with jitter
                await HumanBehavior.jitter_delay(200, 600)
                
                if any(k in descriptor for k in ["first name", "firstname"]):
                    await field.fill(user_identity.get("full_name", "").split()[0])
                elif any(k in descriptor for k in ["last name", "lastname"]):
                    await field.fill(user_identity.get("full_name", "").split()[-1])
                elif "full name" in descriptor:
                    await field.fill(user_identity.get("full_name", ""))
                elif "email" in descriptor:
                    await field.fill(user_identity.get("email", ""))
                elif "phone" in descriptor:
                    await field.fill(user_identity.get("phone", ""))
                elif "linkedin" in descriptor:
                    links = user_identity.get("structured_data", {}).get("links", {})
                    await field.fill(links.get("linkedin", ""))
                elif "github" in descriptor:
                    links = user_identity.get("structured_data", {}).get("links", {})
                    await field.fill(links.get("github", ""))
                elif any(k in descriptor for k in ["resume", "cv", "upload"]):
                    resume_path = user_identity.get("resume_path")
                    if resume_path and os.path.exists(resume_path):
                        await self.log(f"Uploading resume: {os.path.basename(resume_path)}", user_id=user_id)
                        await field.set_input_files(resume_path)
                    else:
                        await self.log("Resume requested but no valid path found. Continuing...", "warning", user_id=user_id)
                else:
                    is_hidden = await field.get_attribute("type") == "hidden"
                    if not is_hidden:
                        questions.append({"descriptor": descriptor, "field": field})
            
            except Exception as e:
                logger.warning(f"Error processing field: {e}")

        if questions:
            await self.log(f"Consulting Hunter AI for {len(questions)} complex questions...", "running", agent="Filling Agent", user_id=user_id)
            from app.ai.llm_client import llm_client
            
            q_texts = [q["descriptor"] for q in questions]
            answers = await llm_client.generate_form_answers(
                user_identity, 
                {"title": "Target Job", "description": "Analyzing dynamic requirements..."},
                q_texts
            )
            
            for i, q in enumerate(questions):
                if i < len(answers):
                    await HumanBehavior.jitter_delay(400, 1200)
                    await q["field"].fill(answers[i].get("answer", ""))

        await self.log("Form filling complete. Verification required.", "success", agent="Filling Agent", user_id=user_id)
        await self.emit_screenshot(page, user_id=user_id)

    async def apply_to_job(self, job_id: str, url: str, platform: str, user_identity: Dict[str, Any], user_id: Optional[int] = None):
        # Neural Risk Guard Integration
        risk_score = user_identity.get("job_risk_score", 0.0)
        red_flags = user_identity.get("job_red_flags", [])
        
        if risk_score > 60:
            await self.log(f"High-Risk Signal Detected ({risk_score}%). Flags: {', '.join(red_flags)}", "warning", agent="Intelligence Guard", user_id=user_id)
            await self.log("Pausing execution for strategic safety review...", "warning", agent="Intelligence Guard", user_id=user_id)
            await self.request_confirmation(job_id, user_id=user_id)
            await self.log("Risk acknowledged by user. Proceeding with extreme caution.", "info", agent="Intelligence Guard", user_id=user_id)

        if self.use_mock:
            await self.log(f"SIMULATION: Stealth Engine active for {url}...", "started", agent="Scout Agent", user_id=user_id)
            await HumanBehavior.jitter_delay(1000, 2000)
            await self.emit_screenshot(user_id=user_id)
            await self.log("SIMULATION: Filling form with human-like jitter...", user_id=user_id)
            await HumanBehavior.jitter_delay(2000, 4000)
            await self.emit_screenshot(user_id=user_id)
            await self.request_confirmation(job_id, user_id=user_id)
            await self.log("SIMULATION: Success!", "success", user_id=user_id)
            return

        from playwright.async_api import async_playwright
        from playwright_stealth import stealth_async
        session_path = self._get_session_path(platform)
        
        await self.log(f"Initializing Elite Stealth Engine...", "started", user_id=user_id)
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                    storage_state=session_path if os.path.exists(session_path) else None,
                    viewport={'width': 1280, 'height': 720}
                )
                page = await context.new_page()
                
                # Apply Stealth
                await stealth_async(page)
                
                await self.log(f"Navigating to {url}...", "running", agent="Scout Agent", user_id=user_id)
                await page.goto(url, wait_until="networkidle")
                await HumanBehavior.scroll_behavior(page)
                await HumanBehavior.mouse_jitter(page)
                await self.emit_screenshot(page, user_id=user_id)
                
                await self.log("Scanning for interaction points...", agent="Scout Agent", user_id=user_id)
                # Improved trigger finding
                selectors = [
                    "button:has-text('Apply')", "button:has-text('Easy Apply')", 
                    "a:has-text('Apply')", "button:has-text('Submit Application')"
                ]
                
                found_trigger = False
                for selector in selectors:
                    try:
                        btn = await page.query_selector(selector)
                        if btn and await btn.is_visible():
                            await self.log(f"Executing trigger: {selector}", agent="Scout Agent", user_id=user_id)
                            await btn.click()
                            await HumanBehavior.jitter_delay(2000, 4000)
                            await self.emit_screenshot(page, user_id=user_id)
                            found_trigger = True
                            break
                    except Exception:
                        continue
                
                if not found_trigger:
                    await self.log("No standard trigger found. Attempting direct form analysis.", "warning", agent="Scout Agent", user_id=user_id)

                await self.fill_form(page, user_identity, user_id=user_id)
                await self.request_confirmation(job_id, user_id=user_id)
                
                await context.storage_state(path=session_path)
                await browser.close()
                await self.log("Application cycle complete.", "success", agent="Submission Agent", user_id=user_id)
            except Exception as e:
                logger.error(f"Automation Critical Failure: {str(e)}")
                await self.log(f"Critical Failure: {str(e)}", "error", user_id=user_id)

automation_service = AutomationService()
