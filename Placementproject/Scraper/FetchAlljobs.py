from sqlalchemy.orm import Session
from database import SessionLocal
import crud
import schemas
from datetime import datetime, timedelta
import re
import logging
# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def fetch_all_jobs_from_db():
    db: Session = SessionLocal()
    try:
        # Assuming crud.get_all_job_postings is a function that fetches all job postings from the database
        all_jobs = crud.get_all_job_postings(db)
        return all_jobs
    except Exception as e:
        logger.error(f"Error fetching jobs from the database: {e}")
        return []
    finally:
        db.close()

def fetch_fresher_jobs():
    db: Session= SessionLocal()
    try:
        jobs= crud.get_all_jobs_fresher(db)
        return jobs
    except Exception as e:
        logger.error(f"Error fetching jobs for Fresher:{e}")
        return []
    finally:
        db.close()

def fetch_experienced_jobs():
    db: Session= SessionLocal()
    try:
        jobs= crud.get_all_jobs_Experienced(db)
        return jobs
    except Exception as e:
        logger.error(f"Error fetching jobs for Fresher:{e}")
        return []
    finally:
        db.close()

def fetch_entrylevel_jobs():
    db: Session= SessionLocal()
    try:
        jobs= crud.get_all_jobs_EntryLevel(db)
        return jobs
    except Exception as e:
        logger.error(f"Error fetching jobs for Fresher:{e}")
        return []
    finally:
        db.close()
