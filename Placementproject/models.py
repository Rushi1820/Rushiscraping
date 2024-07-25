# models.py

from sqlalchemy import Column, Integer, String
from database import Base

class JobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    years_of_experience = Column(String)
    company = Column(String)
    job_link = Column(String)  # Add this line
    posted_on=Column(String)
    description = Column(String)
