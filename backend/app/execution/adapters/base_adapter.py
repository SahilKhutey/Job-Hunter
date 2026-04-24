class BaseAdapter:
    """Interface for Site Application Adapters."""
    
    def open_job(self, page, job: dict):
        raise NotImplementedError

    def click_apply(self, page):
        raise NotImplementedError

    def fill_form(self, page, user_profile: dict):
        raise NotImplementedError

    def submit(self, page):
        raise NotImplementedError
