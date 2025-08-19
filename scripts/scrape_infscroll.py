import asyncio
import pandas as pd
from playwright.async_api import async_playwright

async def scrape_infinite_scroll():
    url = "https://quotes.toscrape.com/scroll"
    data = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)

        prev_height = 0
        while True:
            # Scroll to bottom
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)  # Give it time to load

            # Take quotes data
            quotes = await page.query_selector_all(".quote")
            for q in quotes[len(data):]:  # take only new quotes
                text = await q.query_selector(".text")
                author = await q.query_selector(".author")
                tags = await q.query_selector_all(".tags .tag")

                data.append({
                    "Quote": await text.inner_text() if text else "",
                    "Author": await author.inner_text() if author else "",
                    "Tags": [await t.inner_text() for t in tags] if tags else []
                })

            # Check whether we've reached the end
            curr_height = await page.evaluate("document.body.scrollHeight")
            if curr_height == prev_height:
                break
            prev_height = curr_height

        await browser.close()

    # Save to Excel
    df = pd.DataFrame(data)
    df.to_excel("data/quotes.xlsx", index=False)
    print(f"✅ Scraping Finish! {len(data)} quotes saved to data/quotes.xlsx")

if __name__ == "__main__":
    asyncio.run(scrape_infinite_scroll())
