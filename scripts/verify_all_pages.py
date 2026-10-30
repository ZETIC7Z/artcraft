import os
import asyncio
from playwright.async_api import async_playwright

PAGES = [
    ("index", "http://localhost:8792/index.html"),
    ("apps", "http://localhost:8792/apps.html"),
    ("download", "http://localhost:8792/download.html"),
    ("pricing", "http://localhost:8792/pricing.html"),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        os.makedirs("branding/verification", exist_ok=True)

        for name, url in PAGES:
            print(f"Checking {name} at {url} ...")
            await page.goto(url, wait_until="networkidle")
            await page.wait_for_timeout(1000)
            shot_path = f"branding/verification/zetica_live_{name}.png"
            await page.screenshot(path=shot_path, full_page=False)
            print(f"  -> Captured {shot_path}")

        await browser.close()
    print("All live page captures verified!")

if __name__ == "__main__":
    asyncio.run(main())
