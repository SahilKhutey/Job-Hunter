import os

def load_session(browser, user_id):
    session_dir = "sessions"
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
        
    path = f"{session_dir}/{user_id}.json"

    try:
        if os.path.exists(path):
            return browser.new_context(storage_state=path)
        else:
            return browser.new_context()
    except Exception as e:
        print(f"Error loading session: {e}")
        return browser.new_context()
