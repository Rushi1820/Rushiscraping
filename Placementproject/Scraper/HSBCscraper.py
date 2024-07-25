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
# import time
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options

# # Set up Chrome options
# chrome_options = Options()
# chrome_options.add_argument("--headless")  # Ensure GUI is not required
# chrome_options.add_argument("--no-sandbox")  # Required for Docker
# chrome_options.add_argument("--disable-dev-shm-usage")  # Required for Docker

# # Set up the Remote WebDriver
# driver = webdriver.Remote(command_executor="http://127.0.0.1:4444/wd/hub",options=chrome_options)
# # Configure logging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

# def extract_years_of_experience(description):
#     experience_pattern = re.compile(r"(\d+(\.\d+)?)\s+year\(s\) of experience")
#     match = experience_pattern.search(description)
#     return match.group(1) if match else ""


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

# def scrape_jobs_from_page(career_link):
#     driver.get(career_link)
#     wait = WebDriverWait(driver, 20)
#     jobs = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@class='article article--result']")))
#         for job_element in job_elements:
#             title_element = job_element.find_element(By.XPATH, ".//h3[@class='article__header__text__title article__header__text__title--8']")
#             job_link_element = job_element.find_element(By.XPATH, ".//h3[@class='article__header__text__title article__header__text__title--8']/a")
#             posted_element = job_element.find_element(By.XPATH, ".//span[@class='article--item']")
#             location_element=job_element.find_element(By.XPATH,".//span[@class='location']")

#             title = title_element.text
#             job_link = job_link_element.get_attribute("href")
#             job_posted = posted_element.text
#             location=location_element.text

#             job = {
#                 "title": title,
#                 "location": location,
#                 "description": "Click on the Apply link will redirect you to the main page to get full details",
#                 "job_link": job_link,
#                 "years_of_experience": "Not Mentioned",
#                 "posted_on": job_posted
#             }
#             jobs.append(job)
#     except Exception as e:
#         logger.error(f"Error scraping {career_link}: {e}")

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

# def scrape_jobs_from_all_pages(base_url):
#     company_name = "HSBC"
#     all_jobs = []

#     driver.get(base_url)
    
#     # Scrape jobs from the base URL
#     jobs = scrape_jobs_from_page(driver.current_url)
#     if jobs:
#         all_jobs.extend(jobs)
#     else:
#         logger.info(f"No jobs found on the base page {driver.current_url}")

#     while True:
#         try:
#             # Attempt to find and click the "Next" button
#             next_button = driver.find_element(By.PARTIAL_LINK_TEXT, "Next")
#             next_url = next_button.get_attribute("href")

#             # Click the "Next" button and wait for the page to load
#             next_button.click()
#             time.sleep(2)  # Short delay to allow the page to load
            
#             # Scrape the new page
#             driver.get(next_url)
#             jobs = scrape_jobs_from_page(driver.current_url)
#             if jobs:
#                 all_jobs.extend(jobs)
#             else:
#                 logger.info(f"No jobs found on the page {driver.current_url}")

#         except StaleElementReferenceException:
#             logger.info("StaleElementReferenceException: Element is no longer available. Trying again...")
#             time.sleep(2)  # Short delay before retrying
#             continue
#         except NoSuchElementException:
#             logger.info("NoSuchElementException: 'Next' button not found. Ending pagination.")
#             break
#         except Exception as e:
#             logger.info(f"Exception occurred while trying to find or click 'Next': {e}")
#             break

#     if all_jobs:
#         save_jobs_to_db(all_jobs, company_name)

#     logger.info(f"Scraped a total of {len(all_jobs)} job postings")
#     driver.quit()
#     return len(all_jobs)
# def run_scraper():
#     base_url = "https://mycareer.hsbc.com/en_GB/external/SearchJobs/?1017=%5B67213%5D&1017_format=812&1020=%5B79341%2C79330%2C79324%2C79334%5D&1020_format=815&listFilterMode=1&pipelineRecordsPerPage=50#anchor__search-jobs"
#     return scrape_jobs_from_all_pages(base_url)

