# schemas.py

import datetime
from pydantic import BaseModel, Field

class JobPostingBase(BaseModel):
    title: str
    location: str
    years_of_experience: str
    posted_on: str
    description: str
    company: str
    job_link: str

class FreshersandInternsBase(BaseModel):
    title: str
    location: str
    years_of_experience: str
    posted_on: str
    description: str
    company: str
    job_link: str
    created_on: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

class FresherPostingCreate(FreshersandInternsBase):
    pass

class FresherPosting(FreshersandInternsBase):
    id: int

    class Config:
        orm_mode: True

class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int

    class Config:
        orm_mode: True
