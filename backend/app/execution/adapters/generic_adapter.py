from app.execution.adapters.base_adapter import BaseAdapter
from app.execution.form_mapper import map_field
import time
import logging

logger = logging.getLogger(__name__)

class GenericAdapter(BaseAdapter):

    def open_job(self, page, job: dict):
        logger.info(f"Opening Job URL: {job.get('url')}")
        page.goto(job.get("url"))
        time.sleep(2) # Anti-ban delay

    def click_apply(self, page):
        try:
            # Look for common apply buttons
            apply_button = page.locator("text=Apply").first
            if apply_button:
                apply_button.click()
                time.sleep(2)
        except Exception as e:
            logger.warning(f"Could not find standard 'Apply' button: {e}")

    def fill_form(self, page, user_profile: dict):
        logger.info("Extracting form inputs...")
        inputs = page.query_selector_all("input")

        for inp in inputs:
            try:
                name = inp.get_attribute("name") or inp.get_attribute("id") or inp.get_attribute("placeholder") or ""
                value = map_field(name, user_profile)

                if value:
                    inp.fill(value)
                    time.sleep(0.5) # Human-like typing delay
            except Exception as e:
                logger.warning(f"Failed to fill input {name}: {e}")

    def submit(self, page):
        logger.info("Form filled. Waiting for user confirmation...")
        # In a real environment, you'd trigger a UI notification here
        # and pause execution using a semaphore or API polling.
        # As per instructions, this mimics the console interaction MVP.
        print("\n=============================================")
        print("REVIEW REQUIRED. PLEASE SUBMIT IN THE BROWSER.")
        print("=============================================\n")
        input("Press Enter in console to complete the workflow and save session...")
