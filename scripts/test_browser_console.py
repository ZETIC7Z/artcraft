import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge')
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        
        console_logs = []
        failed_requests = []
        
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))
        page.on('requestfailed', lambda req: failed_requests.append(f'FAILED: {req.url} - {req.failure}'))
        
        print('Navigating to http://localhost:8792/ ...')
        await page.goto('http://localhost:8792/', wait_until='domcontentloaded', timeout=10000)
        await asyncio.sleep(2)
        
        await page.screenshot(path='branding/verification/live_page_check.png', full_page=False)
        print(f'Console logs ({len(console_logs)}):')
        for log in console_logs:
            print('  ', log)
        print(f'Failed requests ({len(failed_requests)}):')
        for f in failed_requests:
            print('  ', f)
            
        await browser.close()
        print('Finished browser test.')

if __name__ == '__main__':
    asyncio.run(main())
