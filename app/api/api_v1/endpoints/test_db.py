import logging
from fastapi import APIRouter

from app.database.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

def init():
    try:
        # Try to create session to check if DB is awake
        db = SessionLocal()
        db.execute("SELECT 1")
        return {"message": "DB OK"}
    except Exception as e:
        logger.error(e)
        raise e

@router.get("/test_db")
def test_db():
    logger.info("Initializing service")
    response = init()
    logger.info("Service finished initializing")
    return response