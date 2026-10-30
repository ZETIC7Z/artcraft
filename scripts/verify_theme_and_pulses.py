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
        
        # 1. Light Mode Check (Default)
        await page.evaluate('window.zeticaApplyTheme("light")')
        await asyncio.sleep(2.5)

        os.makedirs('branding/verification', exist_ok=True)
        # Capture Light Mode with Neon Pulses and Bottom-Right Queue
        await page.screenshot(path='branding/verification/live_light_mode_neon.png')
        print('Captured branding/verification/live_light_mode_neon.png')

        # 2. Dark Mode Check (Toggle to Dark Mode)
        print('Switching to Dark Mode via zeticaToggleTheme() ...')
        await page.evaluate('window.zeticaApplyTheme("dark")')
        await asyncio.sleep(2.5)

        # Capture Dark Mode with White Monogram, Neon Pulses, and Bottom-Right Queue
        await page.screenshot(path='branding/verification/live_dark_mode_white_logo.png')
        print('Captured branding/verification/live_dark_mode_white_logo.png')

        # 3. Test Scroll with Bottom-Right Queue & Active Highlights
        await page.evaluate('window.scrollTo({ top: 400, behavior: "smooth" })')
        await asyncio.sleep(1.5)
        await page.screenshot(path='branding/verification/live_dark_mode_scrolled.png')
        print('Captured branding/verification/live_dark_mode_scrolled.png')

        # 4. Check Logo Filter in Dark Mode
        logo_filter = await page.evaluate('''() => {
            const wmLogo = document.querySelector("#wm-letter-0 img");
            const navLogo = document.querySelector(".themed-logo");
            return {
                wmLogoFilter: wmLogo ? getComputedStyle(wmLogo).filter : "not found",
                navLogoFilter: navLogo ? getComputedStyle(navLogo).filter : "not found",
                theme: document.documentElement.getAttribute("data-theme")
            };
        }''')
        print('Logo computed styles in dark mode:', logo_filter)

        print(f'Console messages ({len(console_logs)}):')
        for log in console_logs:
            print('  ', log)

        await browser.close()
        print('Theme and pulse verification completed successfully.')

if __name__ == '__main__':
    asyncio.run(main())
