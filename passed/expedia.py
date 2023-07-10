#import webdriver
import os
from selenium import webdriver
import chromedriver_binary
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import By method to find the elements
from selenium.webdriver.common.by import By
#import time library to give sleep time to load data(bcz if we try to extract the data before getting loaded then we may get errros)
import time
import csv
from webdriver_manager.chrome import ChromeDriverManager
#basically selenium uses a bot for automation and it opens a browser window when run the code so to remove the window we have to import and set options
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
import json
#importing requests
import requests
#importing beautifulsoup for scraping
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service 
#from webdriver_manager.firefox import GeckoDriverManager
#geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
service = Service(ChromeDriverManager().install())
firefox_options = Options()
#firefox_options.binary_location = os.environ["PATHCHROME"]
#firefox_options.binary_location = './firefox/firefox'
import os
#os.chmod('./firefox/firefox', 0o755)
# firefox_options.binary_location = geckodriver_path
#setting the --headless argument to stop the browser window from opening as selenium is a type of automated browser software it opens browser window when we run code
firefox_options.add_argument("--headless")
firefox_options.add_argument("--no-sandbox")
firefox_options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=firefox_options,service=service)
url = 'https://careers.expediagroup.com/jobs/?filter[category]=Technology'
driver.get(url)
L = []
driver.implicitly_wait(20)
time.sleep(2)
num_str = driver.find_element(By.XPATH, "//span[@id='totresultsspan']").get_attribute('innerHTML')
int_num=int(num_str)
#print(int_num)

while True:
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total = soup.find_all("li", class_="Results__list__item")
    #print(total)
    #print(len(total))
    for i in total:
        soup2 = BeautifulSoup(str(i), "html.parser")
        job_title = soup2.find("h3", class_='Results__list__title text-md').text   
        job_link = soup2.find("a")["href"]
        if 'https' not in job_link:
            job_link='https://careers.expediagroup.com/jobs/'+job_link
        job_department = soup2.find("p", class_="Results__list__team text-body").text
        job_location = soup2.find("p", class_="Results__list__location text-body").text.strip()
        L.append({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print({"job_title":job_title, "job_link":job_link, "job_department":job_department, "job_location":job_location})
        #print(len(L))
    try:
        elem=driver.find_element(By.XPATH,"//button[@class='Results__button button button--blue-7']")
        driver.execute_script('arguments[0].click();', elem)
        time.sleep(2)
    except:
        #print("no button?")
        driver.quit()
        break

    if len(L)>=int_num:
        #print('done')
        driver.quit()
        break

#print(len(L))

json_data=json.dumps({'company':'expedia','data':L})
print(json_data)
driver.quit()