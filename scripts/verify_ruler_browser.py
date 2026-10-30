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

        # Ensure Dark Mode First
        print("Ensuring Dark Mode...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
                window.dispatchEvent(new CustomEvent('zetica-theme-change', { detail: { theme: 'dark' } }));
            }
        """)
        await asyncio.sleep(1.0)

        # 1. Dark Mode at Scroll 0
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        await asyncio.sleep(0.8)
        await page.screenshot(path="branding/verification/live_dark_scroll_0.png")
        print("Captured branding/verification/live_dark_scroll_0.png")

        # 2. Dark Mode at Scroll 350px (ZETICA in flight, APPS riding vertically)
        await page.evaluate("window.scrollTo({ top: 350, behavior: 'instant' })")
        await asyncio.sleep(0.8)
        await page.screenshot(path="branding/verification/live_dark_scroll_350.png")
        print("Captured branding/verification/live_dark_scroll_350.png")

        # 3. Dark Mode at Scroll 1000px (ZETICA APPS active)
        await page.evaluate("window.scrollTo({ top: 1000, behavior: 'instant' })")
        await asyncio.sleep(0.8)
        await page.screenshot(path="branding/verification/live_dark_scroll_1000.png")
        print("Captured branding/verification/live_dark_scroll_1000.png")

        # 4. Dark Mode at Features Section (~2400px)
        await page.evaluate("""
            const el = document.getElementById('features');
            if (el) el.scrollIntoView({ behavior: 'instant' });
            else window.scrollTo({ top: 2400, behavior: 'instant' });
        """)
        await asyncio.sleep(0.8)
        await page.screenshot(path="branding/verification/live_dark_scroll_features.png")
        print("Captured branding/verification/live_dark_scroll_features.png")

        # 5. Switch to Light Mode
        print("Switching to Light Mode...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('light');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                window.dispatchEvent(new CustomEvent('zetica-theme-change', { detail: { theme: 'light' } }));
            }
        """)
        await asyncio.sleep(1.0)
        await page.screenshot(path="branding/verification/live_light_scroll_features.png")
        print("Captured branding/verification/live_light_scroll_features.png")

        # 6. Light Mode at Scroll 0
        await page.evaluate("window.scrollTo({ top: 0, behavior: 'instant' })")
        await asyncio.sleep(0.8)
        await page.screenshot(path="branding/verification/live_light_scroll_0.png")
        print("Captured branding/verification/live_light_scroll_0.png")

        # Metrics check
        ruler_mounted = await page.evaluate("!!document.getElementById('zetica-ruler-instrument')")
        flow_mounted = await page.evaluate("!!document.getElementById('zetica-heading-flow')")
        ruler_ticks = await page.evaluate("document.querySelectorAll('.ruler-tick-row').length")
        flow_words = await page.evaluate("document.querySelectorAll('.flow-word-box').length")

        print(f"Ruler Instrument mounted: {ruler_mounted}")
        print(f"Ruler Ticks count: {ruler_ticks}")
        print(f"HeadingFlow mounted: {flow_mounted}")
        print(f"Flow Words count: {flow_words}")

        await browser.close()
        print("Verification completed successfully!")

if __name__ == '__main__':
    asyncio.run(main())
