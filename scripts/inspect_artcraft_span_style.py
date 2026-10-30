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
            const span = document.querySelector('div.pointer-events-none.fixed.inset-0.z-40 span.font-display');
            if (!span) return 'No span';
            const cs = window.getComputedStyle(span);
            return {
                className: span.className,
                style: span.getAttribute('style'),
                fontSize: cs.fontSize,
                fontWeight: cs.fontWeight,
                fontFamily: cs.fontFamily,
                letterSpacing: cs.letterSpacing,
                transform: cs.transform,
                lineHeight: cs.lineHeight,
                width: cs.width,
                height: cs.height
            };
        }""")
        print("Span Computed Style:", data)

asyncio.run(main())
