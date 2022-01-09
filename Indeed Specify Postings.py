import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent

options = Options()
options.add_argument("window-size=1400,1400")
options.add_experimental_option("detach", True)

ua = UserAgent()
userAgent = ua.random
print(userAgent)
options.add_argument(f'user-agent={userAgent}')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

PATH = "C://Program Files (x86)//chromedriver.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)
driver.maximize_window()

jobtitles = []
companies = []
locations = []
descriptions = []

for i in range(0,10,10):
        driver.get('https://www.indeed.com/jobs?q=chemical%20engineer&l=united%20states&start='+str(i))
        driver.implicitly_wait(5)

        jobs = driver.find_elements_by_class_name("slider_container")

        for job in jobs:

                jobtitle = job.find_element_by_class_name('jobTitle').text.replace("new", "").strip()
                jobtitles.append(jobtitle)

                company = job.find_element_by_class_name('companyName').text.replace("new", "").strip()
                companies.append(company)

                location = job.find_element_by_class_name('companyLocation').text.replace("new", "").strip()
                locations.append(location)

        for item in range(15):
                try:
                    popup_path = '/html/body/div[5]/div[1]/button'
                    popup = driver.find_element_by_xpath(popup_path)
                    popup.click()
                except:
                        pass
                time.sleep(5)

                try:
                        job_description_click_path = f'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[5]/div/a[{item + 1}]'
                        job_description_click = driver.find_element_by_xpath(job_description_click_path).click()
                except:
                        job_description_click_path_2 = f'/html/body/table[2]/tbody/tr/td/table/tbody/tr/td[1]/div[4]/div/a[{item + 1}]'
                        job_description_click_2 = driver.find_element_by_xpath(job_description_click_path_2).click()

                iframe = driver.find_element_by_id('vjs-container-iframe')
                driver.switch_to.frame(iframe)
                description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class = "jobsearch-jobDescriptionText"]')))
                description0 = description.get_attribute('innerText')
                print(description0)
                driver.switch_to.default_content()
                descriptions.append(description0)

df_da = pd.DataFrame()
df_da['JobTitle'] = jobtitles
df_da['Company'] = companies
df_da['Location'] = locations
df_da['Description'] = descriptions

df_da_cleaned = df_da.replace({'Description': {'\n': ''}, 'Location': {'\n': ' ', '\+': '', 'location': '', 'locations': '', '\(.*\)': '', '[0-9]': ''}, 'JobTitle': {'CHEMICAL ENGINEER': 'Chemical Engineer', '\(.*\)': ''}}, regex=True)

df_da_cleaned['Location'] = df_da_cleaned['Location'].str.replace(' s ', '', regex=False)

df_da_cleaned['JobTitle'].str.strip()
df_da_cleaned['Company'].str.strip()
df_da_cleaned['Location'].str.strip()
df_da_cleaned['Description'].str.strip()

print(df_da_cleaned['Location'])
print(df_da_cleaned['Company'])
print(df_da_cleaned['JobTitle'])

df_da.to_csv('test_scrape.csv', index=False, encoding='utf-8')
