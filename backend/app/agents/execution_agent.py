import asyncio
import logging
import os
from playwright.async_api import async_playwright, BrowserContext, Page
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class ExecutionAgent:
    """
    The low-level browser automation engine. 
    Handles session persistence, stealth navigation, and DOM interaction.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.user_data_dir = f"sessions/user_{user_id}"
        self.playwright = None
        self.browser = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def start(self, headless: bool = True):
        """Starts the browser with a persistent context."""
        os.makedirs(self.user_data_dir, exist_ok=True)
        
        self.playwright = await async_playwright().start()
        # Using launch_persistent_context to maintain login state (cookies, localStorage)
        self.context = await self.playwright.chromium.launch_persistent_context(
            user_data_dir=self.user_data_dir,
            headless=headless,
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        self.page = self.context.pages[0] if self.context.pages else await self.context.new_page()
        logger.info(f"ExecutionAgent started for user {self.user_id}")

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
        await asyncio.sleep(2) # Human-like pause

    async def get_page_content(self) -> str:
        """Returns the inner text of the page for AI analysis."""
        return await self.page.content()

    async def fill_input(self, selector: str, value: str):
        """Types into a field with a natural delay between keystrokes."""
        await self.page.click(selector)
        await self.page.type(selector, value, delay=100)

    async def click_element(self, selector: str):
        """Clicks an element."""
        await self.page.click(selector)
        await asyncio.sleep(1)

    async def upload_file(self, selector: str, file_path: str):
        """Uploads a file (e.g., resume)."""
        async with self.page.expect_file_chooser() as fc_info:
            await self.page.click(selector)
        file_chooser = await fc_info.value
        await file_chooser.set_files(file_path)

    async def screenshot(self, name: str):
        """Takes a screenshot for debugging or user preview."""
        path = f"static/screenshots/{self.user_id}_{name}.png"
        os.makedirs("static/screenshots", exist_ok=True)
        await self.page.screenshot(path=path)
        return path
