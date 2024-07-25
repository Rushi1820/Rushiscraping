from sqlalchemy.orm import Session
import models, schemas
from sqlalchemy.exc import SQLAlchemyError
from models import JobPosting
from typing import List, Dict
from sqlalchemy import and_, or_


def create_job_posting(db: Session, job_posting: schemas.JobPostingCreate):
    db_job_posting = models.JobPosting(
        title=job_posting.title,
        location=job_posting.location,
        years_of_experience=job_posting.years_of_experience,
        posted_on=job_posting.posted_on,
        description=job_posting.description,
        company=job_posting.company,
        job_link=job_posting.job_link
    )
    try:
        db.add(db_job_posting)
        db.commit()
        db.refresh(db_job_posting)
        print(f"Job posting for {job_posting.title} saved successfully.")
    except SQLAlchemyError as e:
        print(f"Error saving job posting: {e}")
        db.rollback()  # Roll back the session in case of error
    return db_job_posting

def job_exists(db: Session, title: str, company: str, posted_on: str, job_link: str):
    return db.query(models.JobPosting).filter(and_(
            models.JobPosting.title == title,
            models.JobPosting.company == company,
            models.JobPosting.posted_on == posted_on,
            models.JobPosting.job_link == job_link
        )
    ).first() is not None


def get_all_job_postings(db: Session):
    try:
        return db.query(JobPosting).all()
    except Exception as e:
        # Log the exception if needed
        logger.error(f"Error fetching all job postings: {e}")
        return []

def get_job_posting(db: Session, job_posting_id: int):
    return db.query(models.JobPosting).filter(models.JobPosting.id == job_posting_id).first()

def get_all_jobs_fresher(db: Session) -> List[Dict]:
    # Define the list of titles to filter
    titles_to_check = [
        "Software Developer", "Junior Developer", "Software Associate Developer", 
        "Software Developer Associate", "Junior Java Developer", "Junior Data Scientist", 
        "Intern", "AI/ML Intern", "Junior Analyst", "Consultant","Trainee Software Engineer","Java Developer", "Python Developer"
    ]

    # Query the database for jobs with either the specified experience level or titles
    jobs = db.query(JobPosting).filter(
        or_(
            JobPosting.years_of_experience == "Fresher",
            JobPosting.title.in_(titles_to_check)
        )
    ).all()

    job_list = []

    for job in jobs:
        job_dict = {
            "company": job.company,
            "id": job.id,
            "location": job.location,
            "posted_on": job.posted_on,
            "title": job.title,
            "years_of_experience": job.years_of_experience,
            "job_link": job.job_link,
            "description": job.description,
        }
        job_list.append(job_dict)

    return job_list


def get_all_jobs_EntryLevel(db: Session) -> List[Dict]:
    jobs = db.query(JobPosting).filter(JobPosting.years_of_experience == "Entry Level").all()
    job_list = []

    for job in jobs:
        job_dict = {
            "company": job.company,
            "id": job.id,
            "location": job.location,
            "posted_on": job.posted_on,
            "title": job.title,
            "years_of_experience": job.years_of_experience,
            "job_link": job.job_link,
            "description": job.description,
        }
        job_list.append(job_dict)

    return job_list

def get_all_jobs_Experienced(db: Session)-> List[Dict]:
    jobs = db.query(JobPosting).filter(JobPosting.years_of_experience == "Experienced Professionals").all()
    job_list = []

    for job in jobs:
        job_dict = {
            "company": job.company,
            "id": job.id,
            "location": job.location,
            "posted_on": job.posted_on,
            "title": job.title,
            "years_of_experience": job.years_of_experience,
            "job_link": job.job_link,
            "description": job.description,
        }
        job_list.append(job_dict)

    return job_list

