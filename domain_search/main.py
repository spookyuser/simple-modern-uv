"""
Domain Search Web Application

A FastAPI-based web application for searching available .com domains
using a SQLite database of registered domains.
"""

import sqlite3
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(title="Domain Search", description="Find available .com domains")

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Database path
DB_PATH = BASE_DIR / "domains.db"


def check_domain_available(domain: str) -> bool:
    """Check if a domain is available (not in the database)."""
    if not DB_PATH.exists():
        raise HTTPException(
            status_code=500,
            detail="Database not found. Please run the setup script first.",
        )

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT domain FROM domains WHERE domain = ?", (domain.lower(),))
    result = cursor.fetchone()
    conn.close()

    return result is None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/search/single")
async def search_single(word: str) -> dict:
    """Search for a single domain name."""
    if not word:
        raise HTTPException(status_code=400, detail="Word parameter is required")

    domain = word.lower().strip()
    if not domain.replace("-", "").isalnum():
        raise HTTPException(status_code=400, detail="Invalid domain name")

    available = check_domain_available(domain)
    return {"domain": f"{domain}.com", "available": available}


@app.get("/api/search/dictionary")
async def search_dictionary(max_length: int = 15) -> dict:
    """Search for available dictionary words."""
    if max_length < 1 or max_length > 30:
        raise HTTPException(status_code=400, detail="max_length must be between 1 and 30")

    # Read system dictionary
    dict_path = Path("/usr/share/dict/words")
    if not dict_path.exists():
        raise HTTPException(
            status_code=500, detail="System dictionary not found at /usr/share/dict/words"
        )

    available_domains: List[str] = []
    with open(dict_path) as f:
        for line in f:
            word = line.strip().lower()
            if 1 <= len(word) <= max_length and word.isalpha():
                if check_domain_available(word):
                    available_domains.append(f"{word}.com")
                    if len(available_domains) >= 100:  # Limit results
                        break

    return {"available": available_domains, "count": len(available_domains)}


@app.get("/api/search/combinations")
async def search_combinations(word1: str, word2: str) -> dict:
    """Search for combination of two words."""
    if not word1 or not word2:
        raise HTTPException(status_code=400, detail="Both word1 and word2 are required")

    combo = (word1 + word2).lower().strip()
    if not combo.isalpha():
        raise HTTPException(status_code=400, detail="Invalid word combination")

    available = check_domain_available(combo)
    return {"domain": f"{combo}.com", "available": available}


@app.get("/api/search/short-combinations")
async def search_short_combinations(max_word_length: int = 4, limit: int = 100) -> dict:
    """Search for combinations of short dictionary words."""
    if max_word_length < 2 or max_word_length > 6:
        raise HTTPException(status_code=400, detail="max_word_length must be between 2 and 6")

    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")

    # Read system dictionary
    dict_path = Path("/usr/share/dict/words")
    if not dict_path.exists():
        raise HTTPException(
            status_code=500, detail="System dictionary not found at /usr/share/dict/words"
        )

    # Get short words
    words: List[str] = []
    with open(dict_path) as f:
        for line in f:
            word = line.strip().lower()
            if 2 <= len(word) <= max_word_length and word.isalpha():
                words.append(word)

    # Check combinations
    available_domains: List[str] = []
    for word1 in words[:50]:  # Limit to prevent long execution
        for word2 in words[:50]:
            if word1 != word2:
                combo = word1 + word2
                if check_domain_available(combo):
                    available_domains.append(f"{combo}.com")
                    if len(available_domains) >= limit:
                        return {
                            "available": available_domains,
                            "count": len(available_domains),
                        }

    return {"available": available_domains, "count": len(available_domains)}


@app.get("/api/search/letter-number")
async def search_letter_number(limit: int = 100) -> dict:
    """Search for letter-number pattern domains (e.g., q7r7.com)."""
    if limit < 1 or limit > 500:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 500")

    available_domains: List[str] = []
    for a in "abcdefghijklmnopqrstuvwxyz":
        for b in "0123456789":
            for c in "abcdefghijklmnopqrstuvwxyz":
                for d in "0123456789":
                    combo = a + b + c + d
                    if check_domain_available(combo):
                        available_domains.append(f"{combo}.com")
                        if len(available_domains) >= limit:
                            return {
                                "available": available_domains,
                                "count": len(available_domains),
                            }

    return {"available": available_domains, "count": len(available_domains)}


@app.get("/api/health")
async def health() -> dict:
    """Health check endpoint."""
    db_exists = DB_PATH.exists()
    return {"status": "healthy", "database_loaded": db_exists}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
