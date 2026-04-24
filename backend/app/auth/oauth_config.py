from authlib.integrations.starlette_client import OAuth
from app.core.config import settings

oauth = OAuth()

# Google Config
oauth.register(
    name="google",
    client_id=getattr(settings, "GOOGLE_CLIENT_ID", "PLACEHOLDER"),
    client_secret=getattr(settings, "GOOGLE_CLIENT_SECRET", "PLACEHOLDER"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# LinkedIn Config
oauth.register(
    name="linkedin",
    client_id=getattr(settings, "LINKEDIN_CLIENT_ID", "PLACEHOLDER"),
    client_secret=getattr(settings, "LINKEDIN_CLIENT_SECRET", "PLACEHOLDER"),
    authorize_url="https://www.linkedin.com/oauth/v2/authorization",
    access_token_url="https://www.linkedin.com/oauth/v2/accessToken",
    client_kwargs={"scope": "r_liteprofile r_emailaddress"},
)
