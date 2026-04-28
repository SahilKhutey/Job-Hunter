from playwright.async_api import async_playwright
from app.execution.adapters.resolver import get_adapter
from app.execution.session_manager import load_session, save_session
from app.execution.tracker import log_application
import logging
import os

logger = logging.getLogger(__name__)

async def run_application(user_id: int, job: dict, profile: dict):
    """
    Core Playwright Execution Engine (Async).
    Handles browser orchestration, adapter resolution, and session state.
    """
    job_id = job.get("id")
    
    try:
        adapter = get_adapter(job.get("url"))
        logger.info(f"Starting execution for Job {job_id} via {adapter.__class__.__name__}")
        log_application(user_id, job_id, "started")

        async with async_playwright() as p:
            # Launch async browser
            browser = await p.chromium.launch(headless=os.getenv("BROWSER_HEADLESS", "True") == "True")
            context = await load_session(browser, user_id)
            page = await context.new_page()

            # 1. Navigate
            await adapter.open_job(page, job)
            
            # 2. Trigger Application Form
            await adapter.click_apply(page)
            
            # 3. Autofill intelligently
            await adapter.fill_form(page, profile)
            
            log_application(user_id, job_id, "awaiting_confirmation")

            # 4. Human-in-the-loop pause / Final Submit
            await adapter.submit(page)

            # 5. Save updated cookies/state
            await save_session(context, user_id)
            await browser.close()
            
            log_application(user_id, job_id, "submitted")
            return {"status": "completed"}
            
    except Exception as e:
        logger.error(f"Execution Engine failed for job {job_id}: {e}")
        log_application(user_id, job_id, "failed")
        raise e
