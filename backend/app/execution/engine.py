from playwright.sync_api import sync_playwright
from app.execution.adapters.resolver import get_adapter
from app.execution.session_manager import load_session
from app.execution.tracker import log_application
import logging

logger = logging.getLogger(__name__)

def run_application(user_id: int, job: dict, profile: dict):
    """
    Core Playwright Execution Engine.
    Handles browser orchestration, adapter resolution, and session state.
    """
    adapter = get_adapter(job.get("url"))
    
    logger.info(f"Starting execution for Job {job.get('id')} via {adapter.__class__.__name__}")
    log_application(user_id, job.get("id"), "started")

    with sync_playwright() as p:
        try:
            # We must use headless=False to allow human interaction in the console/browser
            browser = p.chromium.launch(headless=False)
            context = load_session(browser, user_id)
            page = context.new_page()

            # 1. Navigate
            adapter.open_job(page, job)
            
            # 2. Trigger Application Form
            adapter.click_apply(page)
            
            # 3. Autofill intelligently
            adapter.fill_form(page, profile)
            
            log_application(user_id, job.get("id"), "awaiting_confirmation")

            # 4. Human-in-the-loop pause
            adapter.submit(page)

            # 5. Save updated cookies/state
            context.storage_state(path=f"sessions/{user_id}.json")
            browser.close()
            
            log_application(user_id, job.get("id"), "submitted")
            return {"status": "completed"}
            
        except Exception as e:
            logger.error(f"Execution Engine failed: {e}")
            log_application(user_id, job.get("id"), "failed")
            raise e # Reraise for Celery retry logic
