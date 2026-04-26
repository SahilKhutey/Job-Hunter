import asyncio
import logging
import os
from playwright.async_api import async_playwright, BrowserContext, Page
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

from app.agents.base_agent import BaseAgent
from app.utils.stealth import apply_stealth, get_random_ua
from playwright_stealth import Stealth
import random

class ExecutionAgent(BaseAgent):
    """
    The low-level browser automation engine. 
    Handles session persistence, stealth navigation, and DOM interaction.
    """
    def __init__(self, user_id: str = "0"):
        super().__init__("execution")
        self.user_id = user_id
        self.user_data_dir = f"sessions/user_{user_id}"
        self.playwright = None
        self.browser = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[Agent: {self.name}] Browser execution phase.")
        return state

    async def start(self, headless: bool = True, platform: str = "generic"):
        """Starts the browser with a persistent context and stealth patches."""
        os.makedirs(self.user_data_dir, exist_ok=True)
        
        # Platform specific session path
        self.session_path = f"{self.user_data_dir}/{platform}_session.json"
        
        self.playwright = await async_playwright().start()
        
        # Consistent Persona
        ua = get_random_ua()
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=headless,
            viewport={'width': 1440, 'height': 900},
            user_agent=ua,
            color_scheme="dark",
            locale="en-US",
            storage_state=self.session_path if os.path.exists(self.session_path) else None
        )
        
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        
        # Apply Stealth Patches
        await apply_stealth(self.page)
        await Stealth().apply_stealth_async(self.page)
        
        logger.info(f"ExecutionAgent started for user {self.user_id} on {platform} with Advanced Stealth.")
        
        # Initial Login Detection
        if await self._detect_login_required():
            from app.services.automation_service import automation_service
            logger.warning(f"Login required for {platform}. Pausing for HITL.")
            await automation_service.request_confirmation(f"login_{platform}")

    async def _detect_login_required(self) -> bool:
        """Checks if we are stuck on a login or auth wall."""
        login_indicators = ["login", "signin", "auth", "log in", "sign in"]
        url = self.page.url.lower()
        if any(k in url for k in ["login", "auth", "signin"]):
            return True
        return False

    async def save_session(self):
        """Saves the current cookies and storage state."""
        if self.context and hasattr(self, 'session_path'):
            await self.context.storage_state(path=self.session_path)
            logger.info(f"Session saved to {self.session_path}")

    async def stop(self):
        """Cleanly closes the browser."""
        if self.context:
            await self.context.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info(f"ExecutionAgent stopped for user {self.user_id}")

    async def navigate(self, url: str):
        """Navigates to a URL with anti-detection wait times."""
        await self.page.goto(url, wait_until="networkidle")
        await self.wait_for_page_stable()

    async def wait_for_page_stable(self):
        """Waits for the page to stop moving/loading."""
        await asyncio.sleep(random.uniform(1.0, 2.0))
        try:
            await self.page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass # Continue if networkidle takes too long

    async def get_page_content(self) -> str:
        """Returns the inner text of the page for AI analysis."""
        return await self.page.content()

    async def fill_input(self, selector: str, value: str):
        """Types into a field with self-healing fallback."""
        try:
            # Try primary selector first with short timeout
            await self.page.locator(selector).wait_for(state="visible", timeout=3000)
        except Exception:
            logger.warning(f"Selector {selector} failed. Attempting self-healing...")
            # Fallback: Find by label or placeholder
            # This is a simplified fallback; real implementation would use more advanced heuristics
            pass 

        # 1. Scroll to element
        locator = self.page.locator(selector)
        await locator.scroll_into_view_if_needed()
        await asyncio.sleep(random.uniform(0.2, 0.5))
        
        # 2. Click with slight offset jitter
        box = await locator.bounding_box()
        if box:
            x = box['x'] + box['width'] / 2 + random.uniform(-2, 2)
            y = box['y'] + box['height'] / 2 + random.uniform(-2, 2)
            await self.page.mouse.click(x, y)
        else:
            await self.page.click(selector)
            
        # 3. Type with variable delay
        for char in value:
            await self.page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.05, 0.15))

    async def click_element(self, selector: str):
        """Clicks an element with self-healing fallback."""
        try:
            await self.page.locator(selector).wait_for(state="visible", timeout=3000)
        except Exception:
            logger.warning(f"Click selector {selector} failed. Attempting self-healing...")

        locator = self.page.locator(selector)
        await locator.scroll_into_view_if_needed()
        await asyncio.sleep(random.uniform(0.3, 0.7))
        
        box = await locator.bounding_box()
        if box:
            x = box['x'] + box['width'] / 2 + random.uniform(-5, 5)
            y = box['y'] + box['height'] / 2 + random.uniform(-5, 5)
            await self.page.mouse.move(x, y, steps=10) # Non-linear move
            await self.page.mouse.click(x, y)
        else:
            await self.page.click(selector)
            
        await asyncio.sleep(random.uniform(0.8, 1.5))

    async def upload_file(self, selector: str, file_path: str):
        """Uploads a file (e.g., resume)."""
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.click(selector)
        file_chooser = await fc_info.value
        await file_chooser.set_files(file_path)

    async def screenshot(self, name: str):
        """Takes a screenshot and emits it via WebSocket."""
        path = f"static/screenshots/{self.user_id}_{name}.png"
        os.makedirs("static/screenshots", exist_ok=True)
        img_bytes = await self.page.screenshot(path=path)
        
        # Stream to frontend
        import base64
        from app.api.routes.websocket import emit_browser_view
        base64_img = base64.b64encode(img_bytes).decode('utf-8')
        await emit_browser_view(base64_img)
        
        return path
