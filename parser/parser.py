import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time


def parse_goldapple_product(url: str) -> dict:
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    driver.get(url)
    time.sleep(20)
    data = {}

    try:
        data['name'] = driver.find_element(By.CSS_SELECTOR, "h1.page-title").text
    except NoSuchElementException:
        data['name'] = None

    try:
        data['price'] = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
    except NoSuchElementException:
        data['price'] = None

    try:
        data['brand'] = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="brand"]').get_attribute("content")
    except NoSuchElementException:
        data['brand'] = None

    try:
        data['description'] = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]').text
    except NoSuchElementException:
        data['description'] = None

    driver.quit()
    return data
