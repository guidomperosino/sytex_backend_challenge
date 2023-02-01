from fastapi import APIRouter
import logging

from app.api.api_v1.endpoints import form_templates, form_instances, test_db

api_router = APIRouter()
logger = logging.getLogger()

api_router.include_router(form_templates.router, prefix="/api/v1/form_templates", tags=["Form Templates"])
api_router.include_router(form_instances.router, prefix="/api/v1/form_instances", tags=["Form Instances"])
api_router.include_router(test_db.router, prefix="/api/v1", tags=["Ping DB"])


@api_router.get("/api/healthcheck", tags= ["API Health Check"])
async def api_health_check():
    return {"message": f"Api Backend Challenge Sytex V 1.0"}
