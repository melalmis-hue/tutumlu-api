from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
from scraper import scrape_akakce, scrape_cimri

app = FastAPI(title="TUTUMLU API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"status": "ok", "message": "TUTUMLU API çalışıyor"}

@app.get("/search")
def search_product(q: str = Query(...)):
    results = scrape_akakce(q) + scrape_cimri(q)
    results.sort(key=lambda x: x["price"])
    return results