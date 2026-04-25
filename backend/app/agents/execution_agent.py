import asyncio
import logging
import os
from playwright.async_api import async_playwright, BrowserContext, Page
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

from app.agents.base_agent import BaseAgent
from app.utils.stealth import apply_stealth, get_random_ua
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

    def run(self, state: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"[Agent: {self.name}] Browser execution phase.")
        return state

    async def start(self, headless: bool = True):
        """Starts the browser with a persistent context and stealth patches."""
        os.makedirs(self.user_data_dir, exist_ok=True)
        
        self.playwright = await async_playwright().start()
        
        # Consistent Persona
        ua = get_random_ua()
        
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=headless,
            viewport={'width': 1440, 'height': 900},
            user_agent=ua,
            color_scheme="dark",
            locale="en-US"
        )
        
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        
        # Apply Stealth Patches
        await apply_stealth(self.page)
        
        logger.info(f"ExecutionAgent started for user {self.user_id} with Stealth enabled.")

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
        await asyncio.sleep(random.uniform(1.5, 3.5)) # Randomized human pause

    async def get_page_content(self) -> str:
        """Returns the inner text of the page for AI analysis."""
        return await self.page.content()

    async def fill_input(self, selector: str, value: str):
        """Types into a field with variable speed mimicking human typing."""
        # 1. Scroll to element
        await self.page.locator(selector).scroll_into_view_if_needed()
        await asyncio.sleep(random.uniform(0.2, 0.5))
        
        # 2. Click with slight offset jitter
        box = await self.page.locator(selector).bounding_box()
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
        """Clicks an element with human-like jitter."""
        await self.page.locator(selector).scroll_into_view_if_needed()
        await asyncio.sleep(random.uniform(0.3, 0.7))
        
        box = await self.page.locator(selector).bounding_box()
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
