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

        scroll_initial = await page.evaluate("window.scrollY")
        print(f"Initial scroll: {scroll_initial}")

        # Hover in the middle of the screen
        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 500)
        await asyncio.sleep(1)

        scroll_after_wheel = await page.evaluate("window.scrollY")
        print(f"Scroll after mouse.wheel(0, 500): {scroll_after_wheel}")

        # Test keyboard arrow down
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("ArrowDown")
        await asyncio.sleep(0.5)
        scroll_after_key = await page.evaluate("window.scrollY")
        print(f"Scroll after keyboard ArrowDown: {scroll_after_key}")

        # Check what lenis exists
        lenis_state = await page.evaluate("""() => {
            return {
                hasLenis: !!window.Lenis,
                has__lenis: !!window.__lenis,
                lenisCurrent: window.__lenis ? {
                    isStopped: window.__lenis.isStopped,
                    isScrolling: window.__lenis.isScrolling,
                    scroll: window.__lenis.scroll,
                    targetScroll: window.__lenis.targetScroll
                } : null
            };
        }""")
        print("Lenis state in page:", lenis_state)

asyncio.run(main())
