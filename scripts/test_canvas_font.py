import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page()
        await page.goto("http://localhost:8792/")
        res = await page.evaluate("""() => {
            const c = document.createElement('canvas');
            const ctx = c.getContext('2d');
            
            // Test setting font with var(--font-archivo)
            ctx.font = '800 34px var(--font-archivo), "Space Grotesk", sans-serif';
            const fontWithVar = ctx.font;
            
            // Test setting font with resolved family
            const resolvedFamily = window.getComputedStyle(document.body).fontFamily;
            ctx.font = `800 34px ${resolvedFamily}`;
            const fontResolved = ctx.font;
            
            const wVar = ctx.measureText('ZETICA APPS').width;
            
            // Measure actual DOM element
            const testEl = document.createElement('span');
            testEl.style.fontFamily = resolvedFamily;
            testEl.style.fontSize = '34px';
            testEl.style.fontWeight = '800';
            testEl.style.letterSpacing = '0.04em';
            testEl.textContent = 'ZETICA APPS';
            document.body.appendChild(testEl);
            const domWidth = testEl.getBoundingClientRect().width;
            testEl.remove();

            return { fontWithVar, fontResolved, wVar, domWidth };
        }""")
        print("Canvas font test results:", res)

asyncio.run(main())
