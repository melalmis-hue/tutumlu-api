import requests
from bs4 import BeautifulSoup
import re
import logging
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'tr-TR,tr;q=0.9,en;q=0.8',
}

def clean_price(text: str) -> Optional[float]:
    if not text: return None
    nums = re.findall(r'(\d+[\.,]?\d*)', text.replace('.', '').replace(',', '.'))
    if nums:
        try: return float(nums[0])
        except: pass
    return None

def scrape_akakce(query: str) -> List[Dict]:
    products = []
    try:
        url = f'https://www.akakce.com/arama/?q={query}'
        logger.info(f"Akakçe'ye istek atılıyor: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        logger.info(f"Akakçe yanıt kodu: {resp.status_code}")
        soup = BeautifulSoup(resp.text, 'html.parser')

        for item in soup.select('li[data-product]'):
            name_tag = item.select_one('h3.pn_v8, h3, span[title]')
            price_tag = item.select_one('span.pt_v8, span.price, p.price')
            if name_tag and price_tag:
                name = name_tag.text.strip()
                price = clean_price(price_tag.text)
                if name and price:
                    products.append({'name': name, 'price': price, 'market': 'Akakçe', 'source': 'Akakçe'})
                    if len(products) >= 10: break
        logger.info(f"Akakçe'den {len(products)} ürün bulundu")
    except Exception as e:
        logger.error(f"Akakçe hatası: {e}")
    return products

def scrape_cimri(query: str) -> List[Dict]:
    products = []
    try:
        url = f'https://www.cimri.com/arama?q={query}'
        logger.info(f"Cimri'ye istek atılıyor: {url}")
        resp = requests.get(url, headers=HEADERS, timeout=15)
        logger.info(f"Cimri yanıt kodu: {resp.status_code}")
        soup = BeautifulSoup(resp.text, 'html.parser')

        for item in soup.select('[class*="ProductCard"], [class*="product-item"], article'):
            name_tag = item.select_one('h3, [class*="title"], [class*="name"]')
            price_tag = item.select_one('[class*="Price"], [class*="price"]')
            if name_tag and price_tag:
                name = name_tag.text.strip()
                price = clean_price(price_tag.text)
                if name and price:
                    products.append({'name': name, 'price': price, 'market': 'Cimri', 'source': 'Cimri'})
                    if len(products) >= 10: break
        logger.info(f"Cimri'den {len(products)} ürün bulundu")
    except Exception as e:
        logger.error(f"Cimri hatası: {e}")
    return products