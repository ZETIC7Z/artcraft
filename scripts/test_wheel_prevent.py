import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://localhost:8792/", wait_until="networkidle")
        await asyncio.sleep(2)

        # Attach capture listeners
        await page.evaluate("""() => {
            window.__wheelLogs = [];
            window.addEventListener('wheel', (e) => {
                window.__wheelLogs.push({
                    phase: 'capture-window',
                    defaultPrevented: e.defaultPrevented,
                    target: e.target ? (e.target.tagName + '.' + e.target.className) : ''
                });
            }, { capture: true, passive: false });

            window.addEventListener('wheel', (e) => {
                window.__wheelLogs.push({
                    phase: 'bubble-window',
                    defaultPrevented: e.defaultPrevented,
                    target: e.target ? (e.target.tagName + '.' + e.target.className) : ''
                });
            }, { capture: false, passive: false });
        }""")

        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(0.5)

        logs = await page.evaluate("window.__wheelLogs")
        print("Wheel logs:", logs)

asyncio.run(main())
