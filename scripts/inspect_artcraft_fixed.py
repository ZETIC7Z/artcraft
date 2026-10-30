import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("https://getartcraft.com/", wait_until="networkidle")
        await asyncio.sleep(2)

        data = await page.evaluate("""() => {
            const canvases = Array.from(document.querySelectorAll('canvas')).map(c => {
                const r = c.getBoundingClientRect();
                return { id: c.id, className: c.className, x: r.x, y: r.y, w: r.width, h: r.height };
            });
            const allFixed = Array.from(document.querySelectorAll('*')).filter(el => {
                const s = window.getComputedStyle(el);
                return s.position === 'fixed';
            }).map(el => {
                const r = el.getBoundingClientRect();
                return { tag: el.tagName, id: el.id, className: el.className, x: r.x, y: r.y, w: r.width, h: r.height, text: el.innerText ? el.innerText.slice(0, 50) : '' };
            });
            return { canvases, allFixed };
        }""")
        print("Canvases:", data['canvases'])
        print("\nFixed elements:")
        for f in data['allFixed']:
            print(f)

asyncio.run(main())
