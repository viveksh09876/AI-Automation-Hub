from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "AI Automation Hub"
    ENV: str = "local"

    DATABASE_URL: str | None = None

    SUPABASE_URL: str | None = None
    SUPABASE_SERVICE_ROLE_KEY: str | None = None

    OPENAI_API_KEY: str | None = None

    N8N_WEBHOOK_BASE_URL: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()