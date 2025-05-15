from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import random
import string
import sqlite3


app = FastAPI()

def init_db():
    conn = sqlite3.connect("url_shortener.db")
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_key TEXT NOT NULL UNIQUE,
            count_clicks INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()


class URLShortener:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000/"
        self.characters = string.ascii_letters + string.digits

    def generate_short_key(self):
        return "".join(random.choices(self.characters, k=6))

    def shorten_url(self, url):
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("SELECT short_key FROM urls WHERE original_url = ?", (url,))
        result = cursor.fetchone()
        if result:
            short_key = result[0]
            conn.close()
            return self.base_url + short_key

        while True:
            short_key = self.generate_short_key()
            cursor.execute("SELECT short_key FROM urls WHERE short_key = ?", (short_key,))
            if not cursor.fetchone():
                break

        cursor.execute("INSERT INTO urls (original_url, short_key) VALUES (?, ?)", (url, short_key))
        conn.commit()
        conn.close()

        return self.base_url + short_key

    def get_original_url(self, short_url):
        short_key = short_url.replace(self.base_url, "")
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("SELECT original_url FROM urls WHERE short_key = ?", (short_key,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return None
    
    def get_click_count(self, short_url):
        short_key = short_url.replace(self.base_url, "")
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("SELECT count_clicks FROM urls WHERE short_key = ?", (short_key,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        return None
    
    def increment_click_count(self, short_url):
        short_key = short_url.replace(self.base_url, "")
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE urls SET count_clicks = count_clicks + 1 WHERE short_key = ?", (short_key,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return False
        return True


    def delete_url(self, short_url):
        short_key = short_url.replace(self.base_url, "")
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM urls WHERE short_key = ?", (short_key,))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return False
        return True

    def update_url(self, short_url, new_url):
        short_key = short_url.replace(self.base_url, "")
        conn = sqlite3.connect("url_shortener.db")
        cursor = conn.cursor()

        cursor.execute("UPDATE urls SET original_url = ? WHERE short_key = ?", (new_url, short_key))
        conn.commit()
        conn.close()

        if cursor.rowcount == 0:
            return False
        return True


init_db()

url_shortener = URLShortener()


@app.post("/shorten_url/")
async def shorten_url(url: str):
    """Create a shortened URL."""
    short_url = url_shortener.shorten_url(url)
    return {"shortened_url": short_url}

@app.get("/{short_url}")
async def redirect_url(short_url: str):
    original_url = url_shortener.get_original_url(short_url)
    if not original_url:
        raise HTTPException(status_code=404, detail="URL not found")
    incremented = url_shortener.increment_click_count(short_url)
    if not incremented:
        raise HTTPException(status_code=500, detail="Failed to increment click count")
    
    return RedirectResponse(url=original_url)

@app.get("/get_click_count/")
async def get_click_count(short_url: str):
    """Retrieve the click count for a shortened URL."""
    click_count = url_shortener.get_click_count(short_url)
    if click_count is not None:
        return {"click_count": click_count}
    raise HTTPException(status_code=404, detail="URL not found")   

@app.get("/get_original_url/")
async def get_original_url(short_url: str):
    original_url = url_shortener.get_original_url(short_url)
    if original_url:
        return {"original_url": original_url}
    raise HTTPException(status_code=404, detail="URL not found")


@app.delete("/delete_url/")
async def delete_url(short_url: str):
    success = url_shortener.delete_url(short_url)
    if success:
        return {"message": "URL deleted successfully"}
    raise HTTPException(status_code=404, detail="URL not found")


@app.put("/update_url/")
async def update_url(short_url: str, new_url: str):
    """Update the original URL associated with a shortened URL."""
    success = url_shortener.update_url(short_url, new_url)
    if success:
        return {"message": "URL updated successfully"}
    raise HTTPException(status_code=404, detail="URL not found")

