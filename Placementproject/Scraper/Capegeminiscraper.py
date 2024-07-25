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
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ensure GUI is not required
# chrome_options.add_argument("--no-sandbox")  # Required for Docker
# chrome_options.add_argument("--disable-dev-shm-usage")  # Required for Docker

# # Set up the Remote WebDriver
# driver = webdriver.Remote(
#     command_executor="http://127.0.0.1:4444/wd/hub",
#     options=chrome_options
# )
# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# # Set up the WebDriver
# def is_within_last_7_days(date_str):
#     date_formats = ["%d %b %Y", "%d %m %Y", "%m %d %Y", "%b %d %Y", "%d %b %Y"]
#     date_posted = None
    
#     for fmt in date_formats:
#         try:
#             date_posted = datetime.strptime(date_str, fmt)
#             break
#         except ValueError:
#             continue
    
#     if date_posted is None:
#         logger.error(f"Date format for '{date_str}' is not recognized.")
#         return False

# def scrape_jobs_from_page(job_link,title):
#     driver.get(job_link)
#     wait = WebDriverWait(driver, 20)
#     jobs = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='col-sm-12 col-md-6 col-lg-12 job-meta-box-detail']")))
        
#         for job_element in job_elements:
#             label = job_element.find_element(By.CLASS_NAME, 'label').text
#             value = job_element.find_element(By.CLASS_NAME, 'value').text
            
#             if label == "Posted on":
#                  posted_element= value
#             elif label == "Experience level":
#                  years_element = value
#             elif label == "Location":
#                  location_element = value


#         description_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'col-sm-12 col-md-12 col-lg-8 article-text')]")))
#         description=description_element.text

#         if is_within_last_7_days(posted_element):
#             job = {
#                 "title": title,
#                 "location": location_element,
#                 "description": description,
#                 "job_link": job_link,
#                 "years_of_experience": years_element,
#                 "posted_on": posted_element
#             }        
#             jobs.append(job)
        
#     except Exception as e:
#         logger.error(f"Error scraping {job_link}: {e}")

#     return jobs

# def save_jobs_to_db(jobs, company_name):
#     db: Session = SessionLocal()
#     for job in jobs:
#         if not crud.job_exists(db, job['title'], company_name, job['posted_on'],job['job_link']):
#             job_data = schemas.JobPostingCreate(
#                 title=job['title'],
#                 location=job['location'],
#                 description=job['description'],
#                 company=company_name,
#                 job_link=job['job_link'],
#                 years_of_experience=job['years_of_experience'],
#                 posted_on=job['posted_on']
#             )
#             crud.create_job_posting(db, job_data)
#         else:
#             logger.info(f"Job '{job['title']}' in '{job['location']}' already exists and will not be saved.")
#     db.close()

# def scrape_job_links_from_page(career_link):
#     driver.get(career_link)
#     wait = WebDriverWait(driver, 20)
#     job_links = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//a[@class='table-tr filter-box tag-active joblink']")))
#         for job_element in job_elements:
#             job_link = job_element.get_attribute("href")
#             title_element = job_element.find_element(By.XPATH, ".//div[@class='table-td table-title']")
#             title = title_element.text.strip()
#             print(title)
#             job_links.append((job_link,title))  # Create and append a tuple
#     except Exception as e:
#         logger.error(f"Error scraping job links from {career_link}: {e}")

#     return job_links

# def scrape_jobs_from_all_pages(base_url):
#     company_name = "Capgemini"
#     all_jobs = []

#     job_links = scrape_job_links_from_page(base_url)
#     if job_links:
#         for job_link,title in job_links:
#             jobs = scrape_jobs_from_page(job_link,title)  # Pass both link and title
#             if jobs:
#                 all_jobs.extend(jobs)
#     else:
#         logger.info(f"No jobs found on the initial page")

#     if all_jobs:
#         save_jobs_to_db(all_jobs, company_name)

#     logger.info(f"Scraped a total of {len(all_jobs)} job postings")
#     return len(all_jobs)

# def run_scraper():
#     base_url = "https://www.capgemini.com/careers/join-capgemini/job-search/?country_code=en-in&country_name=India&size=5"
#     return scrape_jobs_from_all_pages(base_url)
