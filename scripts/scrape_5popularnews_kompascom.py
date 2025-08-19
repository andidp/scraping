import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL halaman populer Detik
url = "https://indeks.kompas.com/terpopuler"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ambil HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Find populer news (judul + link)
berita = []
for item in soup.select("div.articleList div.articleItem a.article-link")[:5]:
    link = item["href"]
    berita.append({"Judul": "", "Link": link, "Link image": ""})
    
i = 0
for item in soup.select("div.articleList div.articleItem a.article-link .articleItem-img img")[:5]:
    linkImage = item["src"]
    berita[i]["Link image"] = linkImage
    i += 1
    
j = 0
for item in soup.select("div.articleList div.articleItem a.article-link .articleTitle")[:5]:
    judul = item.get_text(strip=True)
    berita[j]["Judul"] = judul
    j += 1

# simpan ke Excel
df = pd.DataFrame(berita)
df.to_excel("data/kompascom_5populernews.xlsx", index=False)

print("✅ Finish, data saved to data/kompascom_5populernews.xlsx")
