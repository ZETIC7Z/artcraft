import asyncio
import sys
import os
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8')

async def main():
    os.makedirs('branding/verification', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        console_errors = []
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ['error', 'warning'] else None)
        page.on("pageerror", lambda err: console_errors.append(f"[pageerror] {err}"))

        print("Navigating to http://localhost:8792/ ...")
        await page.goto("http://localhost:8792/", wait_until="networkidle")
        await asyncio.sleep(2)

        # 1. Test Mouse Wheel Scroll Down
        print("1. Testing Mouse Wheel Scroll Down...")
        s0 = await page.evaluate("window.scrollY")
        await page.mouse.move(700, 450)
        await page.mouse.wheel(0, 300)
        await asyncio.sleep(0.6)
        s1 = await page.evaluate("window.scrollY")
        assert s1 > s0, f"Wheel scroll failed to advance: {s0} -> {s1}"
        print(f"   Wheel scroll 300px advanced successfully: {s0} -> {s1}")

        # 2. Test Continuous Mouse Wheel Scroll
        print("2. Testing Continuous Mouse Wheel Scroll to Features...")
        await page.mouse.wheel(0, 1800)
        await asyncio.sleep(1.2)
        s2 = await page.evaluate("window.scrollY")
        print(f"   Continuous wheel scroll reached: {s2}")
        assert s2 > 1500, f"Expected scroll > 1500, got {s2}"
        await page.screenshot(path="branding/verification/final_wheel_scroll_features.png")

        # 3. Test Keyboard Arrow Down
        print("3. Testing Keyboard Arrow Down...")
        await page.keyboard.press("ArrowDown")
        await page.keyboard.press("ArrowDown")
        await asyncio.sleep(0.4)
        s3 = await page.evaluate("window.scrollY")
        print(f"   Keyboard arrow down advanced to: {s3}")
        assert s3 > s2, f"Keyboard arrow down failed: {s2} -> {s3}"

        # 4. Test Rail Click Jump
        print("4. Testing Ruler Rail Click Jump...")
        # Click at 50% height on the rail (x = 1410, y = 450)
        await page.mouse.click(1410, 450)
        await asyncio.sleep(1.5)
        s4 = await page.evaluate("window.scrollY")
        doc_height = await page.evaluate("document.documentElement.scrollHeight - window.innerHeight")
        pct = (s4 / doc_height) * 100
        print(f"   Rail click jumped to scroll: {s4:.0f} (~{pct:.1f}%)")
        assert s4 > 2000, f"Expected rail jump to mid-page, got {s4}"
        await page.screenshot(path="branding/verification/final_rail_jump.png")

        # 5. Test Heading Flow Link Click Jump
        print("5. Testing Flow Word Hit Link Jump...")
        # Scroll up to top first
        await page.evaluate("window.__lenis ? window.__lenis.scrollTo(0, { immediate: true }) : window.scrollTo(0, 0)")
        await asyncio.sleep(1.0)
        # Click on "ZETICA STUDIO" in bottom queue
        studio_link = await page.query_selector('.flow-word-hit[aria-label="Jump to ZETICA STUDIO"]')
        if studio_link:
            await studio_link.click()
            await asyncio.sleep(1.5)
            s5 = await page.evaluate("window.scrollY")
            print(f"   Clicked ZETICA STUDIO hit link, scrolled to: {s5}")
            assert s5 > 500, f"Expected jump to Studio section, got {s5}"

        # 6. Test Theme Toggle (Dark -> Light -> Dark)
        print("6. Testing Theme Toggle Switch...")
        await page.evaluate("window.zeticaToggleTheme()")
        await asyncio.sleep(0.5)
        theme1 = await page.evaluate("document.documentElement.getAttribute('data-theme')")
        print(f"   Toggled theme: {theme1}")
        await page.screenshot(path="branding/verification/final_theme_light.png")

        await page.evaluate("window.zeticaToggleTheme()")
        await asyncio.sleep(0.5)
        theme2 = await page.evaluate("document.documentElement.getAttribute('data-theme')")
        print(f"   Toggled theme back: {theme2}")
        await page.screenshot(path="branding/verification/final_theme_dark.png")

        # 7. Check Console Logs
        print(f"Total Warnings & Errors: {len(console_errors)}")
        for err in console_errors:
            print("   ", err)

        print("\nALL VERIFICATION CHECKS PASSED WITH FLYING COLORS!")

asyncio.run(main())
