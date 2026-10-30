import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8791', wait_until='networkidle')
        await asyncio.sleep(2)
        await page.screenshot(path=r'c:\Users\ZETICUZ\Documents\artcraft\branding\preview_current.png', full_page=False)
        print('Captured preview_current.png successfully with Edge!')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture())
