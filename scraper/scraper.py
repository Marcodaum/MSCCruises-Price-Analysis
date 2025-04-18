from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from scraper.cruise import Cruise as cruiseClass
from random import randint
from time import sleep


def scrape():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.msccruises.de/Search%20Result?passengers=2%7C0%7C0%7C0&page=1')

    print("Waiting for site to load up...")
    search_results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "cruise-card-info__inner"))
    )

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    pages = int(soup.find_all("li", attrs={"class": "number", "data-v-82963a40": True})[-1].find("a").text.strip())
    cruise_list = []

    for page in range(pages):
        sleep(randint(1,10))
        driver.get('https://www.msccruises.de/Search%20Result?passengers=2%7C0%7C0%7C0&page=' + str(page + 1))
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "cruise-card-info__inner"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        cruises = soup.find_all("section", {"class": "cruise-card-info__inner"})
        for cruise in cruises:
            cruise_id = cruise.find(attrs={"data-v-68983be6": True, "data-v-ec16924a": True})["cruise-id"]
            cruise_name = " ".join(cruise.find("span", {"class": "ship-name"}).text.strip().split(' ')[1:])
            cruise_duration = cruise.find(attrs={"data-v-00ce0371": True}).text.strip().split(' ')[0]
            cruise_price = cruise.find("span", {"class": "prices__main-price"}).find("span").text.strip().split(' ')[1].replace('.', '')
            cruise_list.append(cruiseClass(cruise_id, cruise_name, cruise_duration, cruise_price))
    return cruise_list
    driver.quit()