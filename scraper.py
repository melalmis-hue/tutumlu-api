import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import time
import random
import os
from typing import List, Dict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _create_driver():
    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium")
    driver = uc.Chrome(options=options)
    return driver

def scrape_akakce(query: str) -> List[Dict]:
    products = []
    driver = None
    try:
        driver = _create_driver()
        url = f'https://www.akakce.com/arama/?q={query}'
        logger.info(f"Akakçe: {url}")
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li[data-product]"))
        )
        time.sleep(random.uniform(2, 4))
        items = driver.find_elements(By.CSS_SELECTOR, "li[data-product]")
        for item in items[:5]:
            try:
                name_el = item.find_element(By.CSS_SELECTOR, "h3")
                price_el = item.find_element(By.CSS_SELECTOR, "span.pt_v8, span.price")
                name = name_el.text.strip()
                price = float(price_el.text.replace(".", "").replace(",", ".").replace("TL", "").strip())
                if name and price:
                    products.append({"name": name, "price": price, "market": "Akakçe", "source": "Akakçe"})
            except Exception:
                continue
        logger.info(f"Akakçe: {len(products)} ürün")
    except Exception as e:
        logger.error(f"Akakçe hata: {e}")
    finally:
        if driver:
            driver.quit()
    return products

def scrape_cimri(query: str) -> List[Dict]:
    products = []
    driver = None
    try:
        driver = _create_driver()
        url = f'https://www.cimri.com/arama?q={query}'
        logger.info(f"Cimri: {url}")
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[class*='ProductCard'], [class*='product-item']"))
        )
        time.sleep(random.uniform(2, 4))
        items = driver.find_elements(By.CSS_SELECTOR, "[class*='ProductCard'], [class*='product-item']")
        for item in items[:5]:
            try:
                name_el = item.find_element(By.CSS_SELECTOR, "h3, [class*='title']")
                price_el = item.find_element(By.CSS_SELECTOR, "[class*='Price'], [class*='price']")
                name = name_el.text.strip()
                price = float(price_el.text.replace(".", "").replace(",", ".").replace("TL", "").strip())
                if name and price:
                    products.append({"name": name, "price": price, "market": "Cimri", "source": "Cimri"})
            except Exception:
                continue
        logger.info(f"Cimri: {len(products)} ürün")
    except Exception as e:
        logger.error(f"Cimri hata: {e}")
    finally:
        if driver:
            driver.quit()
    return products