import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL halaman populer Detik
url = "https://www.republika.co.id/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ambil HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find populer news (judul + link)
berita = []
for item in soup.select("div.terpopuler tr.list-terpopuler a")[:5]:
    link = item["href"]
    title = item.get_text(strip=True)
    berita.append({"Judul": title, "Link": link, "Link image": ""})

# Save to Excel
df = pd.DataFrame(berita)
df.to_excel("data/republika_5populernews.xlsx", index=False)

print("✅ Finish, data saved to data/republika_5populernews.xlsx")
