from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import datetime
from .producer import produce_data

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")  # important for running in Docker
options.add_argument("--disable-dev-shm-usage")  # important for Docker

URL = 'https://www.cryptocompare.com/coins/list/all/USD/1'

def scrape():
    with webdriver.Chrome(options=options) as driver:
        driver.get(URL)
        trs = driver.find_elements(By.CSS_SELECTOR, "tr.ng-scope")

        currencies = []
        try:
            for i, tr in enumerate(trs):
                if i == 10:
                    break

                tds = tr.find_elements(By.CSS_SELECTOR, "td")

                currency = {
                    "place": tds[0].find_element(By.XPATH, "div").text,
                    "name": tds[2].find_element(By.CSS_SELECTOR, "h3").text,
                    "price": tds[3].find_element(By.XPATH, "div").text,
                    "volume": tds[5].find_element(By.XPATH, "div").text,
                    "top_tier_volume": tds[6].find_element(By.XPATH, "div").text,
                    "market_cap": tds[7].find_element(By.XPATH, "div").text,
                    "percentage_change": tds[9].find_element(By.XPATH, "div").text
                }

                currencies.append(currency)

            # save the informations to json
            feed = {
                "timestamp": str(datetime.now()),
                "data": currencies
            }
            # produce the data to the broker
            produce_data('crypto.cryptocompare', feed)
            
        except Exception as error:
            print(error)