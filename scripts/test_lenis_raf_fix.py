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

        # Before fix
        scroll0 = await page.evaluate("window.scrollY")
        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(0.5)
        scroll_before = await page.evaluate("window.scrollY")
        print(f"Before RAF hook: scroll went from {scroll0} to {scroll_before}")

        # Now test hooking lenis.raf in requestAnimationFrame
        await page.evaluate("""() => {
            if (window.Lenis) {
                const lenis = new window.Lenis({ lerp: 0.1 });
                window.__lenis = lenis;
                function raf(time) {
                    lenis.raf(time);
                    requestAnimationFrame(raf);
                }
                requestAnimationFrame(raf);
            }
        }""")
        await asyncio.sleep(0.5)

        # Now test mouse wheel with raf hooked!
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(1.0)
        scroll_after = await page.evaluate("window.scrollY")
        print(f"After RAF hook: scroll went from {scroll_before} to {scroll_after}!")

asyncio.run(main())
