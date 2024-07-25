# import re
# import logging
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
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

# def wait_for_element_to_be_stale(driver, element, timeout=20):
#     try:
#         wait = WebDriverWait(driver, timeout)
#         wait.until(EC.staleness_of(element))
#     except StaleElementReferenceException:
#         pass
#     except NoSuchElementException:
#         pass

# def fetch_element_with_retry(driver, locator, retries=3):
#     attempt = 0
#     while attempt < retries:
#         try:
#             return driver.find_element(*locator)
#         except StaleElementReferenceException:
#             attempt += 1
#             logger.info(f"Retrying fetch for element: {locator} (attempt {attempt}/{retries})")
#     return None

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
    
#     return (datetime.now() - date_posted).days <= 7

# def scrape_job_details(job_link, title):
#     driver.get(job_link)
#     wait = WebDriverWait(driver, 20)

#     # Define locators
#     description_locator = (By.XPATH, "//div[@class='col-lg-8 main-col']/article")
#     posted_locator = (By.XPATH, "//dt[text()='Date published:']/following-sibling::dd")
#     location_locator = (By.XPATH, "//dt[text()='Location:']/following-sibling::dd")

#     try:
#         description_element = fetch_element_with_retry(driver, description_locator)
#         posted_element = fetch_element_with_retry(driver, posted_locator)
#         location_element = fetch_element_with_retry(driver, location_locator)

#         if description_element and posted_element and location_element:
#             description = description_element.text
#             job_posted = posted_element.text
#             location = location_element.text
#             if is_within_last_7_days(job_posted):
#              job = {
#                 "title": title,
#                 "location": location,
#                 "description": description,
#                 "job_link": job_link,
#                 "years_of_experience": "Not Mentioned",
#                 "posted_on": job_posted
#              }
#              return job
#         else:
#             raise Exception("Failed to fetch job details elements.")
#     except Exception as e:
#         logger.error(f"Error scraping job details from {job_link}: {e}")
#         return None

# def scrape_job_links_from_page(career_link):
#     driver.get(career_link)
#     wait = WebDriverWait(driver, 20)
#     job_links = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='card-body']")))
#         for job_element in job_elements:
#             job_link_element = job_element.find_element(By.XPATH, ".//a[@class='stretched-link js-view-job']")
#             job_link = job_link_element.get_attribute("href")
#             title_element = job_element.find_element(By.XPATH, ".//h2[@class='card-title']")
#             title = title_element.text
#             job_links.append((job_link, title))
#     except Exception as e:
#         logger.error(f"Error scraping job links from {career_link}: {e}")

#     return job_links

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

# def scrape_jobs_from_page(career_link, page_number):
#     company_name = "Cognizant"
#     all_jobs = []

#     logger.info(f"Scraping jobs for {company_name} from page {page_number}")

#     page_url = career_link.format(page_number=page_number)
#     job_links = scrape_job_links_from_page(page_url)
#     if job_links:
#         for job_link, title in job_links:
#             job = scrape_job_details(job_link, title)
#             if job:
#                 all_jobs.append(job)
#     else:
#         logger.info(f"No jobs found on page {page_number}")

#     if all_jobs:
#         save_jobs_to_db(all_jobs, company_name)

#     logger.info(f"Scraped a total of {len(all_jobs)} job postings from page {page_number}")
#     return len(all_jobs)

# def run_scraper():
#     base_url = "https://careers.cognizant.com/global-en/jobs/?page={page_number}&location=India&cname=India&ccode=IN&origin=global#results"
#     total_pages = 5  # Adjust this value based on the number of pages you want to scrape

#     total_jobs_scraped = 0
#     for page_number in range(1, total_pages + 1):
#         jobs_scraped = scrape_jobs_from_page(base_url, page_number)
#         total_jobs_scraped += jobs_scraped

#     driver.quit()
#     logger.info(f"Scraped a total of {total_jobs_scraped} job postings from {total_pages} pages")
#     return total_jobs_scraped


# def fetch_all_jobs_from_db():
#     db: Session = SessionLocal()
#     try:
#         # Assuming crud.get_all_job_postings is a function that fetches all job postings from the database
#         all_jobs = crud.get_all_job_postings(db)
#         return all_jobs
#     except Exception as e:
#         logger.error(f"Error fetching jobs from the database: {e}")
#         return []
#     finally:
#         db.close()
