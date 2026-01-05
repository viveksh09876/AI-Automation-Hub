import logging
from fastapi import FastAPI, Depends
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.dependencies import get_settings
from app.core.version import APP_VERSION

setup_logging()

logger = logging.getLogger("app.main")

app = FastAPI(
  title = settings.APP_NAME,
  debug = settings.ENV == "local",
  lifespan=lifespan
)

@app.get("/health")
def health_check(app_settings=Depends(get_settings)):
  logger.info("Health check requested")
  return { "status": "ok", "environment": app_settings.ENV }

@app.get("/info")
def service_info(app_settings=Depends(get_settings)):
    return {
        "app": app_settings.APP_NAME,
        "version": APP_VERSION,
        "environment": app_settings.ENV
    }