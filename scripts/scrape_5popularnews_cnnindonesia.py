import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL halaman populer Detik
url = "https://www.cnnindonesia.com"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# Take HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find populer news (judul + link)
berita = []
for item in soup.select("article.relative a.group")[:5]:
    link = item["href"]
    
    h2_tag = item.select_one("h2")
    title = h2_tag.get_text(strip=True) if h2_tag else "N/A"
    berita.append({"Judul": title, "Link": link, "Link image": ""})

# Save to Excel
df = pd.DataFrame(berita)
df.to_excel("data/cnnindonesia_5populernews.xlsx", index=False)

print("✅ Finish, data saved to data/cnnindonesia_5populernews.xlsx")
