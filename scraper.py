import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional

def clean_price(text: str) -> Optional[float]:
    """Fiyat metnini temizleyip float'a çevirir."""
    if not text:
        return None
    # Noktayı ayır, virgülü noktaya çevir
    cleaned = text.replace('.', '').replace(',', '.').replace('TL', '').replace('₺', '').strip()
    try:
        return float(cleaned)
    except ValueError:
        nums = re.findall(r'(\d+[\.,]?\d*)', text)
        if nums:
            return float(nums[0].replace(',', '.'))
    return None

def scrape_akakce(query: str) -> List[Dict]:
    """Akakçe'den ürün ve fiyat çeker."""
    products = []
    try:
        url = f'https://www.akakce.com/arama/?q={query}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.select('li[data-product]'):
            name_tag = item.select_one('h3.pn_v8, h3.product-title, span[title]')
            price_tag = item.select_one('span.pt_v8, span.price, p.price')
            market_tag = item.select_one('span.go_v8, span.merchant, img[alt]')

            name = name_tag.text.strip() if name_tag else None
            price = clean_price(price_tag.text) if price_tag else None
            market = market_tag.get('alt') or market_tag.text.strip() if market_tag else 'Akakçe'

            if name and price:
                products.append({
                    'name': name,
                    'price': price,
                    'market': market,
                    'source': 'Akakçe'
                })
                if len(products) >= 5:
                    break
    except Exception:
        pass
    return products

def scrape_cimri(query: str) -> List[Dict]:
    """Cimri'den ürün ve fiyat çeker."""
    products = []
    try:
        url = f'https://www.cimri.com/arama?q={query}'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        for item in soup.select('[class*="ProductCard"], [class*="product-item"], article'):
            name_tag = item.select_one('h3, [class*="title"], [class*="name"]')
            price_tag = item.select_one('[class*="Price"], [class*="price"]')

            name = name_tag.text.strip() if name_tag else None
            price = clean_price(price_tag.text) if price_tag else None

            if name and price:
                products.append({
                    'name': name,
                    'price': price,
                    'market': 'Cimri Piyasa',
                    'source': 'Cimri'
                })
                if len(products) >= 5:
                    break
    except Exception:
        pass
    return products