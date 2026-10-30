import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge')
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})

        console_logs = []
        page.on('console', lambda msg: console_logs.append(f'[{msg.type}] {msg.text}'))

        print('Navigating to http://localhost:8792/ ...')
        await page.goto('http://localhost:8792/', wait_until='domcontentloaded')
        
        # Wait 2.5s for intro animation and 3D galaxy render
        await asyncio.sleep(2.5)

        os.makedirs('branding/verification', exist_ok=True)
        # Capture Hero at rest with 3D Galaxy
        await page.screenshot(path='branding/verification/hero_3d_galaxy_live.png')
        print('Captured branding/verification/hero_3d_galaxy_live.png')

        # Scroll down 250px to test wordmark transfer
        await page.evaluate('window.scrollTo({ top: 250, behavior: "smooth" })')
        await asyncio.sleep(1.2)
        await page.screenshot(path='branding/verification/hero_wordmark_scroll_250px.png')
        print('Captured branding/verification/hero_wordmark_scroll_250px.png')

        # Scroll down 500px to test features section with galaxy passing
        await page.evaluate('window.scrollTo({ top: 500, behavior: "smooth" })')
        await asyncio.sleep(1.2)
        await page.screenshot(path='branding/verification/features_scroll_500px.png')
        print('Captured branding/verification/features_scroll_500px.png')

        print(f'Console messages ({len(console_logs)}):')
        for log in console_logs:
            print('  ', log)

        await browser.close()
        print('Verification run complete.')

if __name__ == '__main__':
    asyncio.run(main())
