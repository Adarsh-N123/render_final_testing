from selenium import webdriver
geckodriver_path = './geckodriver.exe'
# webdriver.gecko.driver = geckodriver_path
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
import json
import requests
from bs4 import BeautifulSoup
import time

firefox_options = Options()
firefox_options.binary_location = './firefox.exe'
firefox_options.add_argument("--headless")
driver = webdriver.Firefox(options=firefox_options,service=FirefoxService(GeckoDriverManager().install()))
url = "https://workday.wd5.myworkdayjobs.com/Workday?jobFamilyGroup=8c5ce7a1cffb43e0a819c249a49fcb00&jobFamilyGroup=a88cba90a00841e0b750341c541b9d56&jobFamilyGroup=4b2f970c50930155b9985193020a0c72"
driver.get(url)
L=[]
driver.implicitly_wait(100)
time.sleep(4)
num_str = driver.find_element(By.XPATH,"//p[@class='css-12psxof']").get_attribute("innerHTML")
ns = ""
for i in num_str:
    if i not in "0123456789":
        break
    else:
        ns+=i
int_num = int(ns)
count = 0
while True:
    
    soup = BeautifulSoup(driver.page_source,"html.parser")
    total = soup.find_all("li",class_='css-1q2dra3')
    # print(len(total))
    # print(total)
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://workday.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
        # print({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    total = soup.find_all("li",class_='css-3hlofn')
    for i in total:
        soup2 = BeautifulSoup(str(i),"html.parser")
        job_title = soup2.find("h3").text
        job_link = "https://workday.wd5.myworkdayjobs.com"+soup2.find("a",class_='css-19uc56f')["href"]
        job_location = soup2.find("dd",class_='css-129m7dg').text
        L.append({"job_title":job_title,"job_location":job_location,"job_link":job_link})
    time.sleep(3)
    try:
        elem = driver.find_element(By.XPATH,"//button[@class='css-ly8o31' and @aria-label='next']")
        driver.execute_script("arguments[0].click();", elem)
        time.sleep(3)
    except:
        break

    
json_data = json.dumps({"company":"workday","data":L})
print(json_data)
driver.quit()




