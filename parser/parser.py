import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def parse_goldapple_product(url: str) -> dict:
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = uc.Chrome(options=options)
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    data = {}

    try:
        name_elem = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'h1._2OI5R span[itemprop="name"]'))
        )
        data['name'] = name_elem.get_attribute("innerText").strip()
    except Exception:
        try:
            fallback_elem = driver.find_element(By.CSS_SELECTOR, "div.x0b3f")
            data['name'] = fallback_elem.get_attribute("innerText").strip()
        except NoSuchElementException:
            data['name'] = None
    try:
        data['brand'] = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="brand"]').get_attribute("content")
    except NoSuchElementException:
        data['brand'] = None

    try:
        data['price'] = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute("content")
    except NoSuchElementException:
        data['price'] = None

    driver.quit()
    return data
