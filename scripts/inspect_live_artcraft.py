import asyncio
import sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        print("Navigating to https://getartcraft.com/ ...")
        await page.goto('https://getartcraft.com/', wait_until='networkidle')
        await asyncio.sleep(2)

        for scroll_y in [0, 500, 1500, 2500, 3800]:
            await page.evaluate(f"window.scrollTo(0, {scroll_y})")
            await asyncio.sleep(0.8)
            await page.screenshot(path=f"branding/verification/artcraft_scroll_{scroll_y}.png")
            info = await page.evaluate("""() => {
                const rightEls = Array.from(document.querySelectorAll('*')).filter(el => {
                    const r = el.getBoundingClientRect();
                    return r.right > 1200 && r.width > 0 && r.height > 0 && el.children.length === 0 && el.textContent.trim().length > 0;
                }).map(el => {
                    const cs = window.getComputedStyle(el);
                    const r = el.getBoundingClientRect();
                    return {
                        text: el.textContent.trim(),
                        font: cs.font,
                        fontSize: cs.fontSize,
                        fontWeight: cs.fontWeight,
                        letterSpacing: cs.letterSpacing,
                        color: cs.color,
                        transform: cs.transform,
                        x: r.x,
                        y: r.y,
                        width: r.width,
                        height: r.height,
                        className: el.className
                    };
                });
                return rightEls;
            }""")
            print(f"\n================ SCROLL {scroll_y} ================")
            # Group by vertical position or text
            grouped = {}
            for item in info:
                txt = item['text']
                if any(k in txt for k in ['ARTCRAFT', 'CRAFTING', 'APPS', 'STUDIO', 'FEATURES', 'OWNERSHIP', 'COMMUNITY', 'GET STARTED', '%']):
                    print(f"[{item['className']}] '{txt}' => font-size: {item['fontSize']}, rendered rect: {item['width']:.1f}x{item['height']:.1f} at ({item['x']:.1f}, {item['y']:.1f}) | transform: {item['transform']}")

asyncio.run(inspect())
