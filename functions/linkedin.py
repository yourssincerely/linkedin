import time
import random
import json
from selenium import webdriver 
from selenium.webdriver.common.by import By

def selenium_firefox(): 
    options = webdriver.FirefoxOptions()
    options.set_preference("dom.webnotifications.serviceworker.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.add_argument("--headless")
    driver = webdriver.Firefox(options = options)
    return driver

def accept_cookies(body):
    page_elements = body.find_elements(By.TAG_NAME, "button")
    cookie_popups = list(filter(lambda x: "Reject" in x.text, page_elements))
    for i in cookie_popups:
        i.click()
    time.sleep(random.randint(8, 15)/10)

def log_in_page(body):
    with open("login/linkedin_login.json") as f:
        data = json.load(f)
        username = data["username"]
        password = data["password"]
    login_username = body.find_elements(By.ID, "username")
    login_username[0].send_keys(username)
    login_password = body.find_elements(By.ID, "password")
    login_password[0].send_keys(password)
    sign_in_buttons = body.find_elements(By.TAG_NAME, "button")
    for i in sign_in_buttons:
        if i.text == "Sign in":
            login_button = i
            break
    login_button.click()
    time.sleep(random.randint(32, 45)/10)

def jobs_page(body):
    a_tags = body.find_elements(By.TAG_NAME, "a")
    for tag in a_tags:
        if tag.text == "Jobs":
            jobs_button = tag
            break
    jobs_button.click()
    time.sleep(random.randint(30,43)/10)

def jobs_page_popup(body):
    a_tags = body.find_elements(By.TAG_NAME, "a")
    for tag in a_tags:
        if "Job alerts" in tag.text:
            job_alert_button = tag
            break
    job_alert_button.click()
    time.sleep(random.randint(22, 29)/10)

def linkedin_job_alerts():
    """
    return: (<selenium.webdriver.remote.webelement.WebElement>, 
        <selenium.webdriver.firefox.webdriver.WebDriver>)

    This function logs in to linkedin taking the login credentials from the file at
        /login/linkedin_login.json
    It navigates to the user's job alerts page and returns a:
        <selenium.webdriver.remote.webelement.WebElement> containing the body of the
        page.
    """
    driver = selenium_firefox()
    driver.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")
    time.sleep(random.randint(23, 34)/10)   
    content = driver.find_elements(By.TAG_NAME, "body")[0]
    accept_cookies(content)
    content = driver.find_elements(By.TAG_NAME, "body")[0]
    log_in_page(content)
    content = driver.find_elements(By.TAG_NAME, "body")[0]
    jobs_page(content)
    content = driver.find_elements(By.TAG_NAME, "body")[0]
    jobs_page_popup(content)
    #content = driver.find_elements(By.TAG_NAME, "body")[0]
    return driver

def job_posts_on_page(body):
    li = body.find_elements(By.TAG_NAME, "li")
    job_posts = list(filter(lambda x: 'jobs-search-results__list-item' in x.get_attribute("outerHTML"), li))
    return job_posts

def get_job_results_page_buttons_total_number(body):
    button_tags = body.find_elements(By.TAG_NAME, "button")
    job_pages = list(filter(lambda x: 'aria-label="Page' in x.get_attribute("outerHTML"), button_tags)) 
    return int(job_pages[-1].text)

def get_next_page_job_button(driver, index):
    button_tags = driver.find_elements(By.TAG_NAME, "button")
    job_pages = list(filter(lambda x: 'aria-label="Page' in x.get_attribute("outerHTML"), button_tags))
    job_page_n_on_page = list(map(lambda x: int(x.get_attribute("outerHTML").split('aria-label="Page ')[1].split('" ')[0]), job_pages))
    job_buttons_with_index = list(zip(job_page_n_on_page, job_pages))
    for button_index in job_buttons_with_index:
        if index == button_index[0]:
            click_me = button_index[1]
            break
    return click_me

def get_job_alert_page(body, 
              job_alert:str):
    a_tags = body.find_elements(By.TAG_NAME, "a")
    for tag in a_tags:
        if tag.text == job_alert:
            target_job_alert = tag
            break
    target_job_alert.click()
    time.sleep(random.randint(31, 42) / 10)

def get_job_info(body):
    """
    body: selenium.webdriver.remote.webelement.WebElement
    
    return: "job_id", "description", "url"
        
    It takes a selenium webelement with the body tag of a linkedin jobs result page 
    and returns a job id, job description and job url.
    """
    target_div = body.find_elements(By.CLASS_NAME, "jobs-unified-top-card__content--two-pane")[0]
    url_elem = list(filter(lambda x: 'href="/jobs' in x.get_attribute("outerHTML"),
                           target_div.find_elements(By.TAG_NAME, "a")))[0]
    url_end = url_elem.get_attribute("outerHTML").split('href="/')[1].split('"')[0]
    url = "https://www.linkedin.com/" + url_end    
    job_id = url_end.split('view/')[1].split('/')[0]
    description_elem = body.find_elements(By.TAG_NAME, "article")[0]
    description = description_elem.text
    return job_id, description, url