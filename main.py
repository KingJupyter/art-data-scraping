from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json

def Find_Element(driver : webdriver.Chrome, by, value : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(by, value)
            break
        except:
            pass
        sleep(0.1)
    return element

def Find_Elements(driver : webdriver.Chrome, by, value : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(by, value)
            if len(elements) > 0:
                break
        except:
            pass
        sleep(0.1)
    return elements

def value_exists(data, value_to_check):
    if data == []:
        return False
    for item in data:
        if item['image_link'] == value_to_check:
            return True
    return False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://lexica.art')

output_data = []
while True:
    art_data = []
    art_list = Find_Elements(driver, By.CSS_SELECTOR, 'div[role="gridcell"]')
    for item in art_list:
        art_link = item.find_element(By.TAG_NAME, 'a').get_attribute('href')
        image_link = item.find_element(By.TAG_NAME, 'img').get_attribute('src')
        print(f'Art Link : {art_link}\nImage Link : {image_link}\n')
        art_data.append({'art_link' : art_link, 'image_link' : image_link})
    for link in art_data:
        if value_exists(output_data, link['image_link']):
            print('This link already exists.\n')
        else:
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(link['art_link'])
            prompt = Find_Element(driver, By.TAG_NAME, 'p').text
            print(prompt + '\n')
            output_data.append({'image_link' : link['image_link'], 'prompt' : prompt})
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            with open('art_link.json', 'w') as data:
                json.dump(output_data, data, indent=4)
    driver.execute_script("window.scrollBy(0, 1000);")
    sleep(3)