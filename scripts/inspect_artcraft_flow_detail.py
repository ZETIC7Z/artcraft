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
            const divs = Array.from(document.querySelectorAll('div.pointer-events-none.fixed.inset-0.z-40'));
            const flowDiv = divs.find(d => (d.textContent || '').includes('CRAFTING') || (d.textContent || '').includes('ARTCRAFT'));
            if (!flowDiv) return { error: 'Not found', allDivs: divs.map(d => ({ text: d.textContent.slice(0, 100), cls: d.className })) };

            const children = Array.from(flowDiv.children).map(c => {
                const spans = Array.from(c.querySelectorAll('span')).map(s => {
                    const cs = window.getComputedStyle(s);
                    const r = s.getBoundingClientRect();
                    return {
                        text: s.textContent,
                        className: s.className,
                        x: r.x,
                        y: r.y,
                        w: r.width,
                        h: r.height,
                        fontSize: cs.fontSize,
                        fontWeight: cs.fontWeight,
                        fontFamily: cs.fontFamily,
                        transform: cs.transform,
                        inlineStyle: s.getAttribute('style')
                    };
                });
                return {
                    tag: c.tagName,
                    className: c.className,
                    inlineStyle: c.getAttribute('style'),
                    spansCount: spans.length,
                    firstSpan: spans[0],
                    allText: (c.textContent || '').replace(/\\s+/g, ' ').trim()
                };
            });
            return { flowDivClass: flowDiv.className, children };
        }""")
        if 'error' in data:
            print("Error:", data)
            return
        print("Flow Div Children:")
        for c in data['children']:
            print(f"\nWord: '{c['allText']}' ({c['spansCount']} spans) | tag: {c['tag']} class: {c['className']}")
            print(f"First span: {c['firstSpan']}")

asyncio.run(main())
