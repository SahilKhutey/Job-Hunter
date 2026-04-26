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

    def tokenize_profile(self, profile: dict) -> tuple[dict, dict]:
        """
        Anonymizes a profile for LLM use and returns a mapping to restore values.
        Returns (anonymized_profile, mapping)
        """
        clean_profile = profile.copy()
        mapping = {}
        
        sensitive_keys = ["email", "phone", "location", "full_name", "first_name", "last_name"]
        for key in sensitive_keys:
            if key in clean_profile and clean_profile[key]:
                token = f"[{key.upper()}_REDACTED]"
                mapping[token] = str(clean_profile[key])
                clean_profile[key] = token
                
        return clean_profile, mapping

    def unmask_value(self, value: str, mapping: dict) -> str:
        """Restores real PII values from redacted tokens."""
        if not value or not isinstance(value, str):
            return value
            
        result = value
        for token, real_value in mapping.items():
            result = result.replace(token, real_value)
            
        return result

privacy_shield = PrivacyShield()
