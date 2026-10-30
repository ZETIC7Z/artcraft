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

        debug_info = await page.evaluate("""() => {
            // Find element at center
            const el = document.elementFromPoint(700, 450);
            
            // Add a spy on wheel event on window and document
            let capturedEvents = [];
            window.addEventListener('wheel', (e) => {
                capturedEvents.push({
                    target: e.target ? (e.target.tagName + '.' + e.target.className) : null,
                    defaultPrevented: e.defaultPrevented,
                    deltaY: e.deltaY
                });
            }, { capture: true, passive: false });

            // Check if Lenis instance exists in local scope or was instantiated
            return {
                elementUnderCursor: el ? {
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    style: el.getAttribute('style')
                } : null
            };
        }""")
        print("Element under cursor:", debug_info)

        # Now trigger mouse wheel and check captured event
        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(0.5)

        wheel_events = await page.evaluate("""() => {
            return window.__lastWheelEvents || 'no captured events var';
        }""")
        print("Wheel events:", wheel_events)

asyncio.run(main())
