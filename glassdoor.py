import json
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import os
import openai

#Enter your open AI API key
openai.api_key = 'open AI API key'

# Type your qualifications, or your resume.
qualification_criteria = """
Tech industry job related mostly to software, requires at most a bachelors degree, requires less than two years of work experience, and no government clearance required. 
"""
#Enter what keywords you want to search on the job page.
search_keywords = "Entry level software engineer"

#Enter a number indicating the time range: Anytime: 0, Last day: 1, Last 3 days: 2, Last week: 3, Last 2 weeks: 4, Last month: 5
date_option = 3

#Enter true for remote only jobs.
remote_only = False

# File to store the job links
output_file = 'qualified.txt'
output_file2 = 'not_qualified.txt'

# Read cookies from the JSON file. Make sure you paste all glassdoor.com site cookies into this file to authenticate!
cookies_file = 'cookies.json'

def analyze_job_posting(job_description, qualification_criteria):
    print("ChatGPT API executed.")
    prompt = f"Given the following job description, tell me true if I am qualified based on the criteria or false if i'm not. Never both: {qualification_criteria}. Job description: {job_description}"
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=50
    )
    
    result = response.choices[0].message.content.strip().lower()
    if 'true' in result:
        return [True, result]
    else:
        return [False, result]

def file_to_dict(file_path):
    file_dict = {}
    with open(file_path, 'r') as file:
        for index, line in enumerate(file):
            clean_line = line.strip()  
            file_dict[clean_line] = index
    return file_dict

# Setting up an updated UserAgent
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

# Configuring the web driver to work in headless mode
driver = Driver(uc=True, log_cdp=True, headless=False, no_sandbox=True, agent=agent, proxy=False)

# URL of the website with search parameters
url = 'https://www.glassdoor.com/Job/index.htm'
driver.get(url)

if os.path.exists(cookies_file):
    with open(cookies_file, 'r') as file:
        cookies = json.load(file)

    # Add cookies to the browser
    for cookie in cookies:
        # Ensure required fields are present and valid
        cookie_dict = {
            'name': cookie.get('name'),
            'value': cookie.get('value'),
            'domain': cookie.get('domain', '.glassdoor.com'),
            'path': cookie.get('path', '/'),
            'secure': cookie.get('secure', True),  
            'httpOnly': cookie.get('httpOnly', True),  
            'sameSite': "None"  
        }
       
        driver.add_cookie(cookie_dict)

    # Refresh the page after adding cookies
    driver.refresh()

    
file_path = 'qualified.txt'
lines_dict = file_to_dict(file_path)
file_path2 = 'not_qualified.txt'
lines_dict2 = file_to_dict(file_path2)

#Type and enter keywords
searchBar = WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.ID, "searchBar-jobTitle"))
    )
searchBar.send_keys(search_keywords)
searchBar.send_keys(Keys.RETURN)

#Close the alert
alert_close = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='job-alert-modal-close']"))
    )
alert_close.click()

#Enter the date
date = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='fromAge']"))
    )
date.click()

date_list_options = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[data-test='fromAge-option']"))
    )
date_list_options[date_option].click()

if remote_only:
    #Click the remote only button
    remote_only_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='remoteWorkType']"))
    )
    remote_only_button.click()
index = 0

with open(output_file, 'a') as file, open(output_file2, 'a') as file2:
    job_elements = WebDriverWait(driver, 120).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-test='jobListing']"))
        )
    
    
    while index < len(job_elements):
        job_elements = WebDriverWait(driver, 120).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-test='jobListing']"))
        )
        if index < len(job_elements):
            # Click on the job listing item
            job_element = job_elements[index]
            WebDriverWait(driver, 120).until(EC.element_to_be_clickable(job_element)).click()
            job_header = job_element.text
            
            jobLink = job_element.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if jobLink in lines_dict or jobLink in lines_dict2:
                print("\n"+"Already in file: "+job_header)

                if index == len(job_elements) - 1:
                    show_more_button = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='load-more']")))
                    show_more_button.click()
                    # Wait for the number of job listings to increase
                    current_job_count = len(job_elements)
                    WebDriverWait(driver, 120).until(
                        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "li[data-test='jobListing']")) > current_job_count
                    )

                    job_elements = WebDriverWait(driver, 120).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-test='jobListing']"))
                    )
                index += 1
                continue
            
            WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.JobDetails_jobDescription__uW_fK:is(.JobDetails_blurDescription__vN7nh, .JobDetails_showHidden__C_FOA)")))
            job_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            job_page_soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_descriptions = job_page_soup.select_one('div.JobDetails_jobDescription__uW_fK:is(.JobDetails_blurDescription__vN7nh, .JobDetails_showHidden__C_FOA)')
            
            if job_descriptions:
                job_description = job_descriptions.get_text()
                job = job_header+job_description
                modelResponse = analyze_job_posting(job, qualification_criteria)
                time.sleep(1)
                if modelResponse[0]:
                    file.write(jobLink+"\n")
                    file.flush()
                else:
                    file2.write(jobLink + "\n")
                    file2.flush()
            
            if index == len(job_elements) - 1:
                try:
                    show_more_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test='load-more']")))
                except:
                    print("No more jobs to load.")
                    index += 1
                    continue

                show_more_button.click()
                # Wait for the number of job listings to increase
                current_job_count = len(job_elements)
                WebDriverWait(driver, 120).until(
                    lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "li[data-test='jobListing']")) > current_job_count
                )

                job_elements = WebDriverWait(driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-test='jobListing']"))
                )
                
        index += 1

# Close the WebDriver

driver.quit()

print(f'Job links saved to {output_file}')

