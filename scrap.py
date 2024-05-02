import os
print("Installing Requirements.....")
os.system("pip install chromedriver-autoinstaller==0.6.4 pandas==2.2.0 selenium==4.18.1")

from time import sleep
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

chromedriver_autoinstaller.install()
options = Options()
driver = webdriver.Chrome(options=options)
url = "https://packaging.python.org/en/latest/guides/section-install/"

driver.get(url)
sleep(1)
urls = []
all_links = driver.find_element(By.CLASS_NAME, "toctree-wrapper.compound")

links = all_links.find_elements(By.TAG_NAME, "a")
for link in links:
    hrefs = link.get_attribute("href")
    urls.append(hrefs)

count = 1
for url in urls:
    driver.get(url)
    sleep(1)
    data = []
    headings = driver.find_elements(By.TAG_NAME, 'h2')
    sub_headings = driver.find_elements(By.TAG_NAME, 'h3')
    commands = driver.find_elements(By.CLASS_NAME, "highlight")
    max_length = max(len(headings), len(sub_headings), len(commands))
    for i in range(max_length):
        if i < len(headings):
            h2_text = headings[i].text
        else:
            h2_text = ""
        
        if i < len(sub_headings):
            h3_text = sub_headings[i].text
        else:
            h3_text=""
        
        if i < len(commands):
            com_text = commands[i].text
        else:
            com_text = ""
            
        if h2_text.strip() or com_text.strip() or h3_text.strip():
            data.append([h2_text, h3_text, com_text])
            
    df = pd.DataFrame(data, columns=['Headings', 'Sub Headings', 'Code'])
    filename = f'site_{count}.csv'
    df.to_csv(filename, index=False)
    print(f"{filename} file has been created successfully.")
    count+=1
driver.close()
