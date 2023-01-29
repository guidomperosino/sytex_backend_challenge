from fastapi import APIRouter
import logging

from app.api.api_v1.endpoints import forms, test_db

api_router = APIRouter()
logger = logging.getLogger()

API_VERSION = "API_VERSION_TO_REPLACE"

api_router.include_router(forms.router, prefix="/api/v1/forms", tags=["Forms"])
api_router.include_router(test_db.router, prefix="/api/v1", tags=["Ping DB"])




@api_router.get("/api/v1/healthcheck", tags= ["API Health Check"])
@api_router.get("/healthcheck", tags= ["API Health Check"])
async def api_health_check():
    return {"message": f"Api Sytex V {API_VERSION}"}
