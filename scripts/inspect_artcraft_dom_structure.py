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

        # Inspect at scroll 0 and scroll 1000
        for s in [0, 800]:
            await page.evaluate(f"window.scrollTo(0, {s})")
            await asyncio.sleep(1)
            dom_data = await page.evaluate("""() => {
                // Find all elements that contain text ARTCRAFT or CRAFTING APPS
                const results = [];
                const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_ELEMENT);
                let node;
                while (node = walker.nextNode()) {
                    const text = node.innerText || '';
                    if (node.children.length === 0 && (
                        text.includes('ARTCRAFT') || 
                        text.includes('CRAFTING') || 
                        text.includes('STUDIO') ||
                        text.includes('OWNERSHIP') ||
                        text.includes('COMMUNITY') ||
                        text.includes('GET STARTED')
                    )) {
                        const r = node.getBoundingClientRect();
                        const cs = window.getComputedStyle(node);
                        results.push({
                            tag: node.tagName,
                            text: text.trim(),
                            className: node.className,
                            id: node.id,
                            parentClass: node.parentElement ? node.parentElement.className : '',
                            grandParentClass: node.parentElement && node.parentElement.parentElement ? node.parentElement.parentElement.className : '',
                            x: r.x,
                            y: r.y,
                            w: r.width,
                            h: r.height,
                            fontSize: cs.fontSize,
                            fontWeight: cs.fontWeight,
                            fontFamily: cs.fontFamily,
                            letterSpacing: cs.letterSpacing,
                            transform: cs.transform,
                            position: cs.position,
                            color: cs.color
                        });
                    }
                }
                return results;
            }""")
            print(f"\n================ DOM AT SCROLL {s} ================")
            for item in dom_data:
                # filter to right-side elements (x > 800)
                if item['x'] > 800 or item['text'] in ['ARTCRAFT', 'CRAFTING APPS']:
                    print(f"[{item['className']}] parent=[{item['parentClass']}] '{item['text']}' @ ({item['x']:.1f}, {item['y']:.1f}, {item['w']:.1f}x{item['h']:.1f})")
                    print(f"   font: {item['fontWeight']} {item['fontSize']} {item['fontFamily']} | letter-spacing: {item['letterSpacing']} | pos: {item['position']} | transform: {item['transform']}")

asyncio.run(main())
