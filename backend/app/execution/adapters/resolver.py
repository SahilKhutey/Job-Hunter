from app.execution.adapters.generic_adapter import GenericAdapter

def get_adapter(url: str):
    """
    Factory pattern to resolve the correct adapter for a given URL.
    """
    if not url:
        return GenericAdapter()

    # E.g., if "linkedin.com" in url: return LinkedInAdapter()
    
    return GenericAdapter()
