
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

import yagmail

import csv

from sys import argv



from webdriver_manager.chrome import ChromeDriverManager

# Import date class from datetime module
from datetime import date

# Returns the current local date
today = date.today()

script, password = argv

URL = "https://in.indeed.com/jobs?q=blue+prism&l=&from=searchOnHP&vjk=cd7b1e100d1b6d63"

#page = requests.get(URL)

#print(page.text)


driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))


wait = WebDriverWait(driver, 10)

driver.get(URL)


get_url = driver.current_url
wait.until(EC.url_to_be(URL))


if get_url == URL:


    page_source = driver.page_source



result = BeautifulSoup(page_source,features="html.parser")

#bp_jobs = result.find_all("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0")
bp_jobs = result.find_all("div", class_="slider_container css-77eoo7 eu4oa1w0")

job_details = []

for bp_job in bp_jobs:
    
    job_detail= {}

       #job_title = bp_job.find("span").text
    job_detail['job_title'] = bp_job.find("a", class_="jcs-JobTitle css-jspxzf eu4oa1w0").text
        
    job_detail["company_name"] = bp_job.find("span", class_="companyName").text
    job_detail["job_location"] = bp_job.find("div", class_="companyLocation").text

    
    job_detail['job_link'] =  "https://in.indeed.com" + bp_job.a['href']

    

    job_details.append(job_detail)
    

filename = 'job_data.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f,['job_title','company_name','job_location', 'job_link'])
    w.writeheader()
    for job_detail in job_details:
        w.writerow(job_detail)


receiver = "divyanduchoubey@gmail.com"
body = "PFA INDEED Job Data FOR RPA DEV Blueprism Role. \n\n Thanks,\n Python Job Bot"


yag = yagmail.SMTP("divyanduchoubey1@gmail.com", password = password)

yag.send(
    to=receiver,
    subject=" TOP RPA Blueprism JOBS on Indeed - " + str(today),
    contents=body, 
    attachments=filename,
)
