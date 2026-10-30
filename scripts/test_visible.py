import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()
        print("Loading localhost:8792 ...")
        await page.goto("http://localhost:8792", wait_until="load")
        await page.add_style_tag(content="""
            [data-reveal], [data-draw-eyebrow] {
                opacity: 1 !important;
                visibility: visible !important;
                transform: none !important;
                filter: none !important;
            }
            [data-draw-rule] {
                transform: scale(1, 1) !important;
            }
            [data-draw-tick] {
                opacity: 1 !important;
                transform: scale(1, 1) !important;
            }
        """)
        await asyncio.sleep(1)
        print("Taking hero screenshot...")
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\test_visible_hero.png")
        print("Taking fullpage screenshot...")
        await page.screenshot(path=r"c:\Users\ZETICUZ\Documents\artcraft\branding\test_visible_full.png", full_page=True)
        print("Done!")
        await browser.close()

asyncio.run(run())
