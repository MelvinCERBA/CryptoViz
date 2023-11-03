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
driver = webdriver.Chrome(options=options)

URL = ''

def scrape():
    produce_data('crypto.crypto2', 'hello')
