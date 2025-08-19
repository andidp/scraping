import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL halaman populer Detik
url = "https://www.detik.com/terpopuler"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# ambil HTML
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# cari berita populer (judul + link)
berita = []
for item in soup.select("article .media__text a.media__link")[:5]:
    judul = item.get_text(strip=True)
    link = item["href"]
    berita.append({"Judul": judul, "Link": link, "Link image": ""})
    
i = 0
for item in soup.select("article .media__image .ratiobox img")[:5]:
    linkImage = item["src"]
    berita[i]["Link image"] = linkImage
    i += 1

# simpan ke Excel
df = pd.DataFrame(berita)
df.to_excel("data/detikcom_5populernews.xlsx", index=False)

print("✅ Selesai, data disimpan ke data/detik_5populernews.xlsx")
