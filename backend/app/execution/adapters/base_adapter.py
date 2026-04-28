class BaseAdapter:
    """Interface for Site Application Adapters (Async)."""
    
    async def open_job(self, page, job: dict):
        raise NotImplementedError

    async def click_apply(self, page):
        raise NotImplementedError

    async def fill_form(self, page, user_profile: dict):
        raise NotImplementedError

    async def submit(self, page):
        raise NotImplementedError
