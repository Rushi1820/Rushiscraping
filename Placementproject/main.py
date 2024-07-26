import logging
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from models import Base
from database import engine
import job_postings
import uvicorn

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Starting FastAPI app")

Base.metadata.create_all(bind=engine)

app = FastAPI()
# Allow all origins for testing purposes. In production, specify the allowed origins.
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_postings.router, prefix="/api/v1", tags=["job_postings"])

if __name__ == "__main__":
    logger.debug("Starting uvicron FastAPI app")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="debug")