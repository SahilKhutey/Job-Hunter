from cryptography.fernet import Fernet
import os
from typing import Optional

class CredentialVault:
    def __init__(self, key: Optional[str] = None):
        # In production, this key should come from an environment variable or KMS
        raw_key = key or os.getenv("VAULT_KEY")
        if not raw_key:
            # Fallback to a generated key if none provided
            self.key = Fernet.generate_key()
        else:
            self.key = raw_key.encode() if isinstance(raw_key, str) else raw_key
            
        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()

# Global vault instance
vault = CredentialVault()
