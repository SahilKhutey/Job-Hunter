import re

class PrivacyShield:
    def __init__(self):
        # Basic patterns for PII
        self.email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
        self.phone_pattern = re.compile(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
        self.address_pattern = re.compile(r'\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Way)\.?')

    def mask_pii(self, text: str) -> str:
        """Masks sensitive information in a string."""
        if not text:
            return text
            
        # Mask Email
        text = self.email_pattern.sub("[EMAIL_REDACTED]", text)
        
        # Mask Phone
        text = self.phone_pattern.sub("[PHONE_REDACTED]", text)
        
        # Mask Address
        text = self.address_pattern.sub("[ADDRESS_REDACTED]", text)
        
        return text

    def anonymize_profile(self, profile: dict) -> dict:
        """Returns a copy of the profile with sensitive fields masked."""
        clean_profile = profile.copy()
        
        sensitive_keys = ["email", "phone", "location", "full_name"]
        for key in sensitive_keys:
            if key in clean_profile and isinstance(clean_profile[key], str):
                clean_profile[key] = f"[{key.upper()}_REDACTED]"
                
        return clean_profile

privacy_shield = PrivacyShield()
