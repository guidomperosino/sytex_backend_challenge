import logging
from fastapi import APIRouter

# from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.database.db import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

max_tries = 5 # 5 seconds
wait_seconds = 1


# @retry(
#     stop=stop_after_attempt(max_tries),
#     wait=wait_fixed(wait_seconds),
#     before=before_log(logger, logging.INFO),
#     after=after_log(logger, logging.WARN),
# )
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