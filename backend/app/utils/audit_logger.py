import logging
import json
import os
from datetime import datetime

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("hunteros.audit")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        fh = logging.FileHandler(os.path.join(LOG_DIR, "audit.log"))
        fh.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(fh)

    def log_event(self, event_type: str, user_id: int, details: dict):
        """Logs a security or automation event as a JSON line."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "user_id": user_id,
            "details": details
        }
        self.logger.info(json.dumps(event))

audit_logger = AuditLogger()
