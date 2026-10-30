import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        
        print("Loading rebranded site at http://localhost:8792 ...")
        await page.goto("http://localhost:8792", wait_until="networkidle")
        await asyncio.sleep(2)

        # 1. Capture Hero
        print("Capturing hero...")
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_live_hero.png")

        # 2. Capture Apps section
        print("Scrolling to apps section...")
        await page.evaluate("window.scrollTo(0, 800)")
        await asyncio.sleep(1)
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_live_apps.png")

        # 3. Capture Studio and Features section
        print("Scrolling to features section...")
        await page.evaluate("window.scrollTo(0, 2200)")
        await asyncio.sleep(1)
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_live_features.png")

        # 4. Capture Footer
        print("Scrolling to footer...")
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await asyncio.sleep(1)
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_live_footer.png")

        # 5. Full page
        print("Capturing full page...")
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_live_full.png", full_page=True)

        print("All screenshots successfully captured!")
        await browser.close()

asyncio.run(verify())
