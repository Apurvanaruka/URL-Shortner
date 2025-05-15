# 🔗 FastAPI URL Shortener

A simple URL shortener API built using **FastAPI** and **SQLite**. It supports URL shortening, redirection, click tracking, and basic CRUD operations.

## 🚀 Features

- Shorten long URLs
- Redirect to the original URL from the short link
- Track how many times a shortened URL has been clicked
- Update the original URL
- Delete shortened URLs
- Get original URL from shortened version

## 🧰 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [Uvicorn](https://www.uvicorn.org/) (ASGI server)
- Python 3.13

## 📁 Project Structure

url\_shortener/
│
├── main.py             # FastAPI app with endpoints
├── url\_shortener.db    # SQLite database (created on first run)
├── README.md           # Project documentation

````

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/your-username/url-shortener.git
cd url-shortener
````

### 2. Install dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install FastAPI and Uvicorn:

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
uvicorn main:app --reload
```

Access the API docs at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📌 API Endpoints

### 🔹 `POST /shorten_url/`

**Description:** Shortens a given URL.

**Query Parameter:**

```
?url=https://example.com
```

**Response:**

```json
{
  "shortened_url": "http://127.0.0.1:8000/abc123"
}
```

---

### 🔹 `GET /{short_url}`

**Description:** Redirects to the original URL and increments the click count.

---

### 🔹 `GET /get_click_count/`

**Description:** Retrieves the number of times the short URL has been clicked.

**Query Parameter:**

```
?short_url=http://127.0.0.1:8000/abc123
```

**Response:**

```json
{
  "click_count": 5
}
```

---

### 🔹 `GET /get_original_url/`

**Description:** Retrieves the original URL from a short URL.

**Query Parameter:**

```
?short_url=http://127.0.0.1:8000/abc123
```

---

### 🔹 `PUT /update_url/`

**Description:** Updates the original URL mapped to a shortened one.

**Query Parameters:**

```
?short_url=http://127.0.0.1:8000/abc123&new_url=https://newsite.com
```

---

### 🔹 `DELETE /delete_url/`

**Description:** Deletes a shortened URL entry.

**Query Parameter:**

```
?short_url=http://127.0.0.1:8000/abc123
```

---

## 📝 Notes

* The short keys are randomly generated (6 alphanumeric characters).
* Click counts are automatically incremented on each redirect.
* Database file (`url_shortener.db`) is created locally.

## 🛡 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

