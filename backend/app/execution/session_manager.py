import os
import json
from app.utils.stealth import get_random_ua

def load_session(browser, user_id):
    session_dir = "sessions"
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
        
    path = f"{session_dir}/{user_id}.json"
    
    # Consistent Persona for the user
    user_agent = get_random_ua()
    viewport = {"width": 1440, "height": 900}
    
    try:
        storage_state = path if os.path.exists(path) else None
        
        return browser.new_context(
            user_agent=user_agent,
            viewport=viewport,
            storage_state=storage_state,
            locale="en-US",
            timezone_id="America/New_York",
            color_scheme="dark"
        )
    except Exception as e:
        print(f"Error loading session: {e}")
        return browser.new_context(user_agent=user_agent, viewport=viewport)

def save_session(context, user_id):
    """Persists cookies and storage state for future runs."""
    session_dir = "sessions"
    os.makedirs(session_dir, exist_ok=True)
    path = f"{session_dir}/{user_id}.json"
    context.storage_state(path=path)
    return path
