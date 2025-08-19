import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL
login_url = "https://quotes.toscrape.com/login"
base_url = "https://quotes.toscrape.com"

# Create session inorder to keep cookies
session = requests.Session()

# --- Step 1: Take csrf token ---
login_page = session.get(login_url)
soup = BeautifulSoup(login_page.text, "html.parser")
csrf_token = soup.find("input", {"name": "csrf_token"})["value"]

# --- Step 2: Login ---
payload = {
    "username": "admin",   # Change based on credentials
    "password": "admin",   # Change based on credentials
    "csrf_token": csrf_token
}
session.post(login_url, data=payload)

# --- Step 3: Scrap all pages (pagination) ---
quotes_data = []
page = 1

while True:
    url = f"{base_url}/page/{page}/"
    res = session.get(url)
    if res.status_code != 200:
        break

    soup = BeautifulSoup(res.text, "html.parser")
    quotes = soup.find_all("div", class_="quote")

    if not quotes:
        break

    for q in quotes:
        text = q.find("span", class_="text").get_text(strip=True)
        author = q.find("small", class_="author").get_text(strip=True)
        tags = [tag.get_text(strip=True) for tag in q.find_all("a", class_="tag")]
        quotes_data.append({
            "Quote": text,
            "Author": author,
            "Tags": ", ".join(tags)
        })

    print(f"✅ Page {page} finished")
    page += 1

# --- Step 4: Save to Excel ---
df = pd.DataFrame(quotes_data)
df.to_excel("data/quotes_login_pagination.xlsx", index=False)

print("✅ All data successfully saved to quotes_login_pagination.xlsx")
