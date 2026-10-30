import os
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("Navigating to http://localhost:8792/download.html ...")
        await page.goto("http://localhost:8792/download.html", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        os.makedirs("branding", exist_ok=True)
        screenshot_path = "branding/zetica_live_download_page.png"
        await page.screenshot(path=screenshot_path, full_page=False)
        print(f"Captured screenshot at {screenshot_path}")

        # Check the href of the download button
        btn = await page.query_selector("a[data-cta], a:has-text('Download for Windows')")
        if btn:
            href = await btn.get_attribute("href")
            print(f"Verified Windows Download Button Href: {href}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
