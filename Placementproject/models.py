# models.py

from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    years_of_experience = Column(String)
    company = Column(String)
    job_link = Column(String)
    posted_on = Column(String)
    description = Column(String)


class FreshersandInterns(Base):
    __tablename__ = "AllJobsFreshersInterns"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    years_of_experience = Column(String)
    company = Column(String)
    job_link = Column(String)
    posted_on = Column(String)
    description = Column(String)
    created_on = Column(DateTime, default=datetime.datetime.utcnow)
