import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        # Inject stack trace logger before any scripts load
        await page.add_init_script("""
            const origPreventDefault = Event.prototype.preventDefault;
            window.__preventLogs = [];
            Event.prototype.preventDefault = function() {
                if (this.type === 'wheel') {
                    const err = new Error();
                    window.__preventLogs.push({
                        type: this.type,
                        target: this.target ? (this.target.tagName + '.' + this.target.className) : '',
                        stack: err.stack
                    });
                }
                return origPreventDefault.apply(this, arguments);
            };
        """)

        await page.goto("http://localhost:8792/", wait_until="networkidle")
        await asyncio.sleep(2)

        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(0.5)

        logs = await page.evaluate("window.__preventLogs")
        print(f"Captured {len(logs)} preventDefault calls on wheel:")
        for l in logs:
            print("--- PREVENT LOG ---")
            print("Target:", l['target'])
            print("Stack:", l['stack'])

asyncio.run(main())
