import asyncio
from playwright.async_api import async_playwright

async def capture_sections():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8791', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Scroll down to footer
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(2)
        await page.screenshot(path=r'c:\Users\ZETICUZ\Documents\artcraft\branding\preview_footer.png', full_page=False)
        print('Captured preview_footer.png!')
        
        # Also capture full page
        await page.screenshot(path=r'c:\Users\ZETICUZ\Documents\artcraft\branding\preview_fullpage.png', full_page=True)
        print('Captured preview_fullpage.png!')
        await browser.close()

if __name__ == '__main__':
    asyncio.run(capture_sections())
