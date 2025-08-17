import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"

def get_categories():
    """Take all categories in nav list"""
    url = urljoin(BASE_URL, "catalogue/category/books_1/index.html")
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    categories = []
    side_menu = soup.select("div.side_categories ul li ul li a")
    for cat in side_menu:
        cat_name = cat.get_text(strip=True)
        cat_url = urljoin(url, cat["href"])
        categories.append((cat_name, cat_url))
    return categories

def get_books_from_category(cat_name, cat_url):
    """Scrape all books from a kategori (multi page)"""
    books = []
    while True:
        resp = requests.get(cat_url)
        soup = BeautifulSoup(resp.text, "html.parser")

        for book in soup.select("article.product_pod"):
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").get_text(strip=True)
            rating = book.p["class"][1]
            availability = book.find("p", class_="instock availability").text.strip()

            books.append({
                "Category": cat_name,
                "Title": title,
                "Price": price,
                "Rating": rating,
                "Availability": availability
            })

        # cek pagination (next)
        next_btn = soup.select_one("li.next a")
        if next_btn:
            cat_url = urljoin(cat_url, next_btn["href"])
        else:
            break
    return books


if __name__ == "__main__":
    all_data = []
    categories = get_categories()

    for cat_name, cat_url in categories:
        print(f"Scraping category: {cat_name}")
        books = get_books_from_category(cat_name, cat_url)
        all_data.extend(books)
            
    df = pd.DataFrame(all_data)

    # === DATA CLEANING ===
    # 1. Clean column price → to float format
    df["Price"] = df["Price"].str.replace("£", "").str.encode("ascii", "ignore").str.decode("ascii").str.replace(r"[^0-9.]", "", regex=True).astype(float)
    
    # 2. Trim whitespace in all text columns
    df["Title"] = df["Title"].str.strip()
    df["Availability"] = df["Availability"].str.strip()

    # 3. Delete duplicate
    df = df.drop_duplicates()

    # 4. Fill empty cell with "N/A"
    df = df.fillna("N/A")

    # === EXPORT TO EXCEL ===
    df.to_excel("data/books_with_category_scraped_clean.xlsx", index=False)

    print("\n✅ Finish! Data already saved to books_scraped_clean.xlsx")
