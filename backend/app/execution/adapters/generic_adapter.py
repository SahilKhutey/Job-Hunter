from app.execution.adapters.base_adapter import BaseAdapter
from app.execution.form_mapper import map_field, map_field_llm
import asyncio
import logging

logger = logging.getLogger(__name__)

class GenericAdapter(BaseAdapter):

    async def open_job(self, page, job: dict):
        logger.info(f"Opening Job URL: {job.get('url')}")
        await page.goto(job.get("url"))
        await asyncio.sleep(2) # Anti-ban delay

    async def click_apply(self, page):
        try:
            # Look for common apply buttons
            apply_button = page.locator("text=Apply").first
            if await apply_button.count() > 0:
                await apply_button.click()
                await asyncio.sleep(2)
        except Exception as e:
            logger.warning(f"Could not find standard 'Apply' button: {e}")

    async def fill_form(self, page, user_profile: dict):
        logger.info("Extracting form inputs...")
        inputs = await page.query_selector_all("input")

        for inp in inputs:
            try:
                name = (await inp.get_attribute("name") or 
                        await inp.get_attribute("id") or 
                        await inp.get_attribute("placeholder") or "")
                
                # Try simple mapping first
                value = map_field(name, user_profile)
                
                # If complex, try LLM mapping
                if not value and name:
                    value = await map_field_llm(name, user_profile)

                if value:
                    await inp.fill(value)
                    await asyncio.sleep(0.5) # Human-like typing delay
            except Exception as e:
                logger.warning(f"Failed to fill input: {e}")

    async def submit(self, page):
        logger.info("Form filled. Waiting for user confirmation...")
        # In the context of a background agent, we might notify via WebSocket
        # and wait for a confirm signal. For now, we'll log it.
        logger.info("--- MANUAL REVIEW REQUIRED IN BROWSER ---")
        # In a real async flow, we would await a confirm event here.
        # For the engine MVP, we'll assume the agent continues after a timeout or manual step.
