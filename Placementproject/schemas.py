# schemas.py

from pydantic import BaseModel

class JobPostingBase(BaseModel):
    title: str
    location: str
    years_of_experience: str
    posted_on: str
    description: str
    company: str
    job_link: str


class JobPostingCreate(JobPostingBase):
    pass

class JobPosting(JobPostingBase):
    id: int

    class Config:
        orm_mode: True
