from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "AI Automation Hub"
    ENV: str = "local"

    DATABASE_URL: Optional[str] | None = None

    SUPABASE_URL: Optional[str] | None = None
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None

    OPENAI_API_KEY: Optional[str] | None = None

    N8N_WEBHOOK_BASE_URL: Optional[str] | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()