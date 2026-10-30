import asyncio
from playwright.async_api import async_playwright

async def inspect_dom():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8791', wait_until='networkidle')
        await asyncio.sleep(2)
        
        # Check if attribution element exists
        el = await page.query_selector('.zeticuz-footer-attribution')
        print('zeticuz-footer-attribution found:', el is not None)
        if el:
            box = await el.bounding_box()
            print('Bounding box:', box)
            visible = await el.is_visible()
            print('Is visible:', visible)
            html = await page.evaluate('el => el.outerHTML', el)
            print('Outer HTML:', html[:200])
        else:
            # Check footer HTML
            footer_html = await page.evaluate('() => document.querySelector("footer") ? document.querySelector("footer").outerHTML : "no footer"')
            print('Footer HTML end:', footer_html[-500:])
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(inspect_dom())
