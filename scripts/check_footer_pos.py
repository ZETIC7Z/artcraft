import asyncio
from playwright.async_api import async_playwright

async def check_footer_pos():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge', headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page.goto('http://localhost:8791', wait_until='networkidle')
        await asyncio.sleep(2)
        
        info = await page.evaluate('''() => {
            const el = document.getElementById('zeticuz-dev-footer');
            if (!el) return { found: false };
            const rect = el.getBoundingClientRect();
            return {
                found: true,
                top: rect.top,
                bottom: rect.bottom,
                left: rect.left,
                width: rect.width,
                height: rect.height,
                parent: el.parentElement.tagName,
                bodyHeight: document.body.scrollHeight,
                windowHeight: window.innerHeight
            };
        }''')
        print('Footer info:', info)
        
        # Scroll to element directly
        if info['found']:
            await page.evaluate('() => document.getElementById("zeticuz-dev-footer").scrollIntoView()')
            await asyncio.sleep(1)
            await page.screenshot(path=r'c:\Users\ZETICUZ\Documents\artcraft\branding\preview_dev_footer.png')
            print('Captured preview_dev_footer.png!')
            
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check_footer_pos())
