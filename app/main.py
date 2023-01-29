from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.api.api_v1.api import api_router

import logging

# Set up Logger
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)

# formatter = logging.Formatter("%(asctime)s %(levelname)-5s  %(message)s")

# handler = logging.StreamHandler()
# handler.setLevel(logging.INFO)
# handler.setFormatter(formatter)
# logger.addHandler(handler)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, log_level="info", reload=True, env_file=".env")