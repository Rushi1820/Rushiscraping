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


# def extract_location(description):
#     # Assuming location follows the pattern "This position is based at our {location} office."
#     location_pattern = re.compile(r"This position is based at our (\w+) office")
#     match = location_pattern.search(description)
#     return match.group(1) if match else ""

# def is_within_last_7_days(date_str):
#     date_formats = ["%d %b %Y", "%d %m %Y", "%m %d %Y", "%b %d %Y", "%d %b %Y"]
#     date_posted = None
    
#     # Check for relative date format "Posted X days ago"
#     match = re.match(r"Posted (\d+) day[s]? ago", date_str)
#     if match:
#         days_ago = int(match.group(1))
#         date_posted = datetime.now() - timedelta(days=days_ago)
#     else:
#         # Try parsing the date with the given formats
#         for fmt in date_formats:
#             try:
#                 date_posted = datetime.strptime(date_str, fmt)
#                 break
#             except ValueError:
#                 continue
    
#     if date_posted is None:
#         logger.error(f"Date format for '{date_str}' is not recognized.")
#         return False
    
#     return (datetime.now() - date_posted).days <= 7

# def scrape_jobs_from_page(career_link):
#     driver.get(career_link)
#     wait = WebDriverWait(driver, 20)
#     jobs = []
#     try:
#         job_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='cmp-teaser card']")))
#         for job_element in job_elements:
#             title_element = job_element.find_element(By.XPATH, ".//h3[@class='cmp-teaser__title']")
#             description_element = job_element.find_element(By.XPATH, ".//span[@class='description']")
#             job_link_element = job_element.find_element(By.XPATH, ".//a[@class='cmp-teaser__title-link']")
#             posted_element = job_element.find_element(By.XPATH, ".//div[@class='cmp-teaser__job-posted']")

#             title = title_element.text
#             description = description_element.text
#             job_link = job_link_element.get_attribute("href")
#             job_posted = posted_element.text


#             years_of_experience = "Entry Level"
#             location = extract_location(description)
#             if is_within_last_7_days(job_posted):
#              job = {
#                 "title": title,
#                 "location": location,
#                 "description": description,
#                 "job_link": job_link,
#                 "years_of_experience": years_of_experience,
#                 "posted_on": job_posted
#              }
#              jobs.append(job)
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

# def scrape_jobs_from_all_pages(base_url, pages):
#     company_name = "Accenture"
#     all_jobs = []

#     for page in range(1, pages + 1):
#         career_link = f"{base_url}&pg={page}"
#         logger.info(f"Scraping jobs for {company_name} from page {page} ({career_link})")
        
#         jobs = scrape_jobs_from_page(career_link)
#         if jobs:
#             all_jobs.extend(jobs)
#         else:
#             logger.info(f"No jobs found on page {page}")
#             break

#     if all_jobs:
#         save_jobs_to_db(all_jobs, company_name)

#     logger.info(f"Scraped a total of {len(all_jobs)} job postings")
#     driver.quit()
#     return len(all_jobs)

# def run_scraper():
#     base_url = "https://www.accenture.com/in-en/careers/jobsearch?jk=&sb=1&vw=0&is_rj=0&sk=consulting|customer%20services|human%20resources|product%20development|software%20engineering|solution%20architecture%20%26%20planning|technology%20%26%20information%20architectures&pd=past%20week&jt=entry-level%20job&et=full-time"
#     num_pages = 10
#     return scrape_jobs_from_all_pages(base_url, num_pages)
