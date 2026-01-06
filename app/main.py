import logging
from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.core.config import settings
from app.core.lifespan import lifespan
from app.core.logging import setup_logging
from app.core.dependencies import get_settings
from app.core.version import APP_VERSION
from app.core.dependencies import get_db
from app.core.auth import get_current_user
from app.api.organizations import router as org_router

setup_logging()

logger = logging.getLogger("app.main")

app = FastAPI(
  title = settings.APP_NAME,
  debug = settings.ENV == "local",
  lifespan=lifespan
)

app.include_router(org_router)

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

@app.get("/db-check")
def db_check(db=Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"db": "connected"}

@app.get("/me")
async def get_me(user=Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
    }