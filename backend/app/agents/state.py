import json
import redis
from app.core.config import settings

class AgentState(dict):
    """
    Shared memory across agents.
    Persists to Redis so asynchronous workers can pick up where they left off.
    """
    def __init__(self, session_id: str, initial_data=None):
        super().__init__()
        self.session_id = f"agent_state:{session_id}"
        self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        
        # Load existing state if any
        stored = self.redis_client.get(self.session_id)
        if stored:
            try:
                self.update(json.loads(stored))
            except json.JSONDecodeError:
                pass
                
        if initial_data:
            self.update(initial_data)
            self._save()

    def update_state(self, key, value):
        self[key] = value
        self._save()
        
    def _save(self):
        # We need to make sure everything is JSON serializable
        try:
            self.redis_client.set(self.session_id, json.dumps(self))
        except Exception as e:
            print(f"Error saving state to Redis: {e}")

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save()
