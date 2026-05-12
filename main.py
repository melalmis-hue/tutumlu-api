from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Optional
from scraper import scrape_akakce, scrape_cimri
import time

app = FastAPI(title="TUTUMLU API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "TUTUMLU API çalışıyor"}

@app.get("/search")
def search_product(
    q: str = Query(..., description="Arama kelimesi")
) -> List[Dict]:
    """Hem Akakçe hem Cimri'den ürün arar ve birleştirir."""
    results = []

    akakce = scrape_akakce(q)
    results.extend(akakce)
    time.sleep(0.3)

    cimri = scrape_cimri(q)
    results.extend(cimri)

    # Fiyata göre sırala
    results.sort(key=lambda x: x['price'])

    return results

@app.get("/markets")
def get_markets() -> List[str]:
    """Desteklenen marketleri listeler."""
    return ["BİM", "A101", "ŞOK", "Migros", "Tarım Kredi"]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)