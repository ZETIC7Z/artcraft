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

        await page.evaluate("window.scrollTo(0, 1400)")
        await asyncio.sleep(0.5)

        data = await page.evaluate("""() => {
            const flowSpans = Array.from(document.querySelectorAll('.flow-letter')).map(el => {
                const cs = window.getComputedStyle(el);
                const r = el.getBoundingClientRect();
                return {
                    char: el.textContent,
                    x: r.x,
                    y: r.y,
                    w: r.width,
                    h: r.height,
                    transform: el.style.transform
                };
            }).filter(s => s.char === 'S' || s.char === 'T' || s.char === 'U');
            return flowSpans;
        }""")
        print("Spans for S, T, U around scroll 1400:")
        for d in data:
            print(d)

asyncio.run(main())
