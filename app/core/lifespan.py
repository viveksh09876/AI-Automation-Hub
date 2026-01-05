from contextlib import asynccontextmanager
import logging
from app.core.config import settings

logger = logging.getLogger("app.lifespan")

@asynccontextmanager
async def lifespan(app):
  logger.info("Starting %s in %s environment", settings.APP_NAME, settings.ENV)

  # app.state.db = init_db()
  # app.state.ai_client = init_ai_client()
  # app.state.webhook_client = init_webhook_client()

  yield

  logger.info("Shutting down %s", settings.APP_NAME)