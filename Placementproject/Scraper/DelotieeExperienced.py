# import re
# import logging
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from sqlalchemy.orm import Session
# from database import SessionLocal
# import crud
# import schemas
# from datetime import datetime, timedelta

# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Set up the WebDriver
# driver = webdriver.Chrome()

# def scrape_jobs_from_page(career_link):
#     driver.get(career_link)
#     wait = WebDriverWait(driver, 20)
#     jobs = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tr[@class='data-row']")))
#         for job_element in job_elements:
#             title_element = job_element.find_element(By.XPATH, ".//span[@class='jobTitle visible-phone']")
#             job_link_element = job_element.find_element(By.XPATH, ".//a[@class='jobTitle-link']")
#             posted_element = job_element.find_element(By.XPATH, ".//span[@class='jobDate visible-phone']")
#             location_element =job_element.find_element(By.XPATH, ".//span[@class='jobLocation visible-phone']")

#             title = title_element.text
#             description = ""
#             job_link = job_link_element.get_attribute("href")
#             job_posted = posted_element.text
#             location=location_element.text


#             job = {
#                 "title": title,
#                 "location": location,
#                 "description": description,
#                 "job_link": job_link,
#                 "posted_on": job_posted
#             }
#             jobs.append(job)
#     except Exception as e:
#         logger.error(f"Error scraping {career_link}: {e}")

#     return jobs

# def save_jobs_to_db(jobs, company_name):
#     db: Session = SessionLocal()  
#     for job in jobs:
#         job_data = schemas.JobPostingCreate(
#             title=job['title'],
#             location=job['location'],
#             description=job['description'],
#             company=company_name,
#             job_link=job['job_link'],
#             years_of_experience="Fresher",
#             posted_on=job['posted_on']
#         )
#         crud.create_job_posting(db, job_data)
#     db.close()

# def scrape_jobs_from_all_pages(base_url):
#     company_name = "Deloitte"
#     all_jobs = []

#     # Scrape jobs from the single page
#     jobs = scrape_jobs_from_page(base_url)
#     if jobs:
#         all_jobs.extend(jobs)
#     else:
#         logger.info(f"No jobs found on the page {base_url}")

#     if all_jobs:
#         save_jobs_to_db(all_jobs, company_name)

#     logger.info(f"Scraped a total of {len(all_jobs)} job postings")
#     driver.quit()
#     return len(all_jobs)

# def run_scraper():
#     base_url = "https://jobsindia.deloitte.com/go/Freshers&apos;-Jobs/548144/"
#     return scrape_jobs_from_all_pages(base_url)
