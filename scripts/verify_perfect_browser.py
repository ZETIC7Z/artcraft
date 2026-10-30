import asyncio
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright

async def main():
    os.makedirs('branding/verification', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))

        print("Navigating to http://localhost:8792/ ...")
        await page.goto("http://localhost:8792/", wait_until="domcontentloaded")
        await asyncio.sleep(2.0)

        # 1. Dark Mode at Scroll 0
        print("Testing Dark Mode at Scroll 0...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_0.png")
        print("Captured branding/verification/perfect_dark_scroll_0.png")

        # 2. Test Resources Dropdown Menu
        print("Opening Resources dropdown menu...")
        await page.click('button[id*="trigger"][id*="ailb"], button:has(svg.lucide-chevron-down)')
        await asyncio.sleep(0.5)
        await page.screenshot(path="branding/verification/perfect_resources_dropdown.png")
        print("Captured branding/verification/perfect_resources_dropdown.png")

        # Close dropdown by clicking body
        await page.click('body', position={'x': 200, 'y': 200})
        await asyncio.sleep(0.5)

        # 3. Scroll to 350px (Wordmark Flight & Riding Rail)
        print("Scrolling to 350px...")
        await page.evaluate("window.scrollTo({ top: 350, behavior: 'instant' })")
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_350.png")
        print("Captured branding/verification/perfect_dark_scroll_350.png")

        # 4. Scroll to Features Section (~2400px)
        print("Scrolling to Features section...")
        await page.evaluate("""
            const el = document.getElementById('features');
            if (el) el.scrollIntoView({ behavior: 'instant' });
            else window.scrollTo({ top: 2400, behavior: 'instant' });
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_features.png")
        print("Captured branding/verification/perfect_dark_scroll_features.png")

        # 5. Scroll to Community / Start Section (~4200px)
        print("Scrolling to Community section...")
        await page.evaluate("""
            const el = document.getElementById('made-with') || document.getElementById('community');
            if (el) el.scrollIntoView({ behavior: 'instant' });
            else window.scrollTo({ top: 4200, behavior: 'instant' });
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_community.png")
        print("Captured branding/verification/perfect_dark_scroll_community.png")

        # 6. Switch to Light Mode
        print("Testing Light Mode at Features...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('light');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/perfect_light_scroll_features.png")
        print("Captured branding/verification/perfect_light_scroll_features.png")

        # Inspect DOM states
        duplicate_check = await page.evaluate("""() => {
            const boxes = document.querySelectorAll('.flow-word-box[data-label="ZETICA"]');
            const mastheads = document.querySelectorAll('#hero-wordmark-masthead');
            const whiteBoxes = document.querySelectorAll('[role="scrollbar"]');
            const dropdown = document.querySelector('.zetica-resources-dropdown');
            return {
                flowWordBoxesForZetica: boxes.length,
                heroMastheads: mastheads.length,
                deadScrollbars: whiteBoxes.length,
                dropdownExists: !!dropdown
            };
        }""")
        print("DOM State Verification:", duplicate_check)

        print(f"Total Console logs: {len(console_logs)}")
        for log in console_logs:
            if "error" in log.lower() or "warn" in log.lower():
                print(" -", log)

        await browser.close()
        print("Comprehensive verification completed!")

if __name__ == '__main__':
    asyncio.run(main())
