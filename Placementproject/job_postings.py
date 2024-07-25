from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
import schemas
from database import SessionLocal
from Scraper import Accenturescraper, Cognizantscraper,DelotieeFresher,HSBCscraper, Capegeminiscraper, FetchAlljobs

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# @router.post("/scrape_jobs/")
# def scrape_jobs():
#     try:
#         num_jobs = Accenturescraper.run_scraper()
#         return {"message": f"Successfully scraped {num_jobs} job postings"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error scraping jobs: {e}")

# @router.post("/scrape_jobs/cognizant")
# def scrape_jobs():
#     try:
#         num_jobs = Cognizantscraper.run_scraper()
#         return {"message": f"Successfully scraped {num_jobs} job postings"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error scraping jobs: {e}")


@router.get("/get_jobs")
def get_jobs():
    try:
        jobs=FetchAlljobs.fetch_all_jobs_from_db()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error fetching jobs:{e}")

# @router.post("/deloitteFresher/scraper")
# def scrape_jobs_deloitte():
#     try:
#         jobs= DelotieeFresher.run_scraper()
#         return {"message":f"Successfully scraped{jobs} job postings"}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")

# @router.post("/HSBC/Scrape_jobs")
# def scrape_jobs():
#     try:
#         jobs=HSBCscraper.run_scraper()
#         return {"message":f"Successfully scraped{jobs} job postings"}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")

# @router.post("/Capegemini/Scrape_jobs")
# def scrape_jobs():
#     try:
#         jobs=Capegeminiscraper.run_scraper()
#         return {"message":f"Successfully scraped{jobs} job postings"}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")


@router.get("/getEntryLeveljobs")
def getEntryLevel():
    try:
        jobs=FetchAlljobs.fetch_entrylevel_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")

@router.get("/getFresherjobs")
def getFresherjobs():
    try:
        jobs=FetchAlljobs.fetch_fresher_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")

@router.get("/getExperiencedjobs")
def getExperiencedjobs():
    try:
        jobs=FetchAlljobs.fetch_experienced_jobs()
        return jobs
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"Error scraping jobs: {e}")