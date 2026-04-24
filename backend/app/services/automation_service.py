import os
import asyncio
import base64
from typing import Dict, Any, Optional
from app.api.routes.websocket import emit_agent_update, manager

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
        except ImportError:
            print("Playwright not found. Automation features will be mocked.")
            self.use_mock = True

    def _get_session_path(self, platform: str) -> str:
        return os.path.join(self.sessions_dir, f"{platform}_session.json")

    async def log(self, message: str, status: str = "running", agent: str = "Hunter AI"):
        print(f"[{agent}] {message}")
        await emit_agent_update(agent, status, message)

    async def request_confirmation(self, job_id: str):
        """Pauses execution and waits for a WebSocket confirmation from the user."""
        event = asyncio.Event()
        self.confirmation_events[job_id] = event
        await self.log("Awaiting manual confirmation for submission...", "warning")
        
        await manager.broadcast({
            "type": "awaiting_confirmation",
            "job_id": job_id,
            "message": "The application is ready. Please review and confirm submission."
        })
        
        # Wait for the event to be set (triggered by another API call or WS message)
        await event.wait()
        del self.confirmation_events[job_id]
        await self.log("Confirmation received. Proceeding with submission.", "success")

    async def confirm_application(self, job_id: str):
        """Triggered by the frontend to resume a paused application."""
        if job_id in self.confirmation_events:
            self.confirmation_events[job_id].set()
            return True
        return False

    async def emit_screenshot(self, page=None):
        """Captures a screenshot and sends it over WS."""
        try:
            if page:
                screenshot = await page.screenshot(type="jpeg", quality=40)
                encoded = base64.b64encode(screenshot).decode('utf-8')
            else:
                # Simulation frame
                encoded = "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAFA3PEY8ED5GWEZGPDpCUXFiS0VUXHdcemZpfHBsfXxlfHpwfh5uYHSUdH1viJqrj4yVmZ5vboqz0561p5mXm5X/2wBDAQlgREBIUHLiYmLi5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mZm5mX/wAARCAABAAEASIAEARED/8QAFQABAQAAAAAAAAAAAAAAAAAAAAf/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFAEBAAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AL+AD//Z"
            
            await manager.broadcast({
                "type": "browser_view",
                "image": encoded
            })
        except Exception as e:
            print(f"Screenshot failed: {e}")

    async def fill_form(self, page, user_identity: Dict[str, Any]):
        """Intelligently fills application forms using heuristics and LLM."""
        await self.log("Analyzing application form...", "running")
        
        # 1. Gather all inputs, textareas, and select elements
        fields = await page.query_selector_all("input, textarea, select")
        questions = []
        field_mapping = []

        for field in fields:
            try:
                # Get associated label or placeholder
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

                # Heuristics for common fields
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
                else:
                    # Treat as a question for LLM if it's a textarea or has a long label
                    if await field.get_attribute("type") != "hidden":
                        questions.append({"descriptor": descriptor, "field": field})
            
            except Exception as e:
                logger.warning(f"Error processing field: {e}")

        # 2. Handle complex questions with LLM
        if questions:
            await self.log(f"Consulting Hunter AI for {len(questions)} complex questions...", "running")
            from app.ai.llm_client import llm_client
            
            # Extract text questions for LLM
            q_texts = [q["descriptor"] for q in questions]
            answers = llm_client.generate_form_answers(
                user_identity, 
                {"title": "Target Job", "description": "Job description not available"}, # Placeholder job context
                q_texts
            )
            
            for i, q in enumerate(questions):
                if i < len(answers):
                    await q["field"].fill(answers[i]["answer"])
                    await asyncio.sleep(0.5)

        await self.log("Form filling complete.", "success")
        await self.emit_screenshot(page)

    async def apply_to_job(self, job_id: str, url: str, platform: str, user_identity: Dict[str, Any]):
        if self.use_mock:
            await self.log(f"SIMULATION: Initializing browser engine for Job {job_id}...", "started")
            await asyncio.sleep(1)
            await self.emit_screenshot()
            await self.log(f"SIMULATION: Navigating to {url}...")
            await asyncio.sleep(2)
            await self.log("SIMULATION: Scanning for application form...")
            await asyncio.sleep(1.5)
            await self.log(f"SIMULATION: Autofilling data for {user_identity.get('full_name')}...")
            await asyncio.sleep(2)
            await self.emit_screenshot()
            
            # HITL Confirmation
            await self.request_confirmation(job_id)
            
            await self.log("SIMULATION: Application submitted successfully!", "success")
            return

        from playwright.async_api import async_playwright
        session_path = self._get_session_path(platform)
        
        await self.log(f"Initializing Hunter AI browser engine...", "started")
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    storage_state=session_path if os.path.exists(session_path) else None,
                    viewport={'width': 1280, 'height': 720}
                )
                page = await context.new_page()
                
                await self.log(f"Navigating to {url}...")
                await page.goto(url, wait_until="networkidle")
                await self.emit_screenshot(page)
                
                await self.log("Scanning page structure...")
                # Basic heuristics for apply buttons
                buttons = await page.query_selector_all("button, a")
                for btn in buttons:
                    text = await btn.inner_text()
                    if any(kw in text.lower() for kw in ["apply", "easy apply", "submit"]):
                        await self.log(f"Found trigger: '{text}'. Executing...")
                        await btn.click()
                        await asyncio.sleep(3)
                        await self.emit_screenshot(page)
                        break
                
                # Intelligent form filling
                await self.fill_form(page, user_identity)
                
                # HITL Confirmation before final submit
                await self.request_confirmation(job_id)
                
                # Resume tracking / Final save
                await context.storage_state(path=session_path)
                await browser.close()
            except Exception as e:
                await self.log(f"Automation Error: {str(e)}", "error")


automation_service = AutomationService()


automation_service = AutomationService()
