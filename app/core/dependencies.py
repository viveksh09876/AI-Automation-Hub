from app.core.config import settings

def get_settings():
    return settings

def get_db():
    """
    Placeholder for DB session.
    """
    db = None
    try:
        yield db
    finally:
        pass


def get_ai_client():
    """
    Placeholder for AI client (OpenAI, etc.).
    """
    ai_client = None
    return ai_client


def get_automation_client():
    """
    Placeholder for n8n or webhook client.
    """
    automation_client = None
    return automation_client
