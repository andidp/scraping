# 📚 Book Categories Scraper

This project is a **Python web scraper** for the website [Books to Scrape](https://books.toscrape.com/).  
It automatically extracts all **categories** and all **books** inside each category (with pagination support).  

---

## 🚀 Features
- Scrapes **all categories** from sidebar navigation.  
- Extracts book details:
  - Category  
  - Title  
  - Price (cleaned to float)  
  - Rating  
  - Availability  
- Handles **pagination** automatically.  
- Cleans and formats data:
  - Converts price to numeric  
  - Removes duplicates  
  - Fills empty cells with `N/A`  
- Exports to **Excel file** (`books_scraped_clean.xlsx`).  

---

## 🛠️ Tech Stack
- Python  
- Requests  
- BeautifulSoup  
- Pandas  

---

## ▶️ Usage
1. Install dependencies:
    
    - For pip
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ``` 
    - For pip3
    ```bash
   pip3 install requests beautifulsoup4 pandas openpyxl
   ``` 
2. Run script:
    - For python (default system)
    ```bash
    python scripts/wcategoryscrapping.py
    ```
    - For python3
    ```bash
    python3 scripts/wcategoryscrapping.py
    ```
