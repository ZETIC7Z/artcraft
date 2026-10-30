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
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ['error'] else None)
        page.on("pageerror", lambda err: console_errors.append(f"[pageerror] {err}"))

        print("Navigating to http://localhost:8792/ ...")
        await page.goto("http://localhost:8792/", wait_until="networkidle")
        await asyncio.sleep(2)

        # Move mouse to center
        await page.mouse.move(720, 450)

        # 1. Scroll down 400px with wheel
        print("1. Wheeling down 400px...")
        await page.mouse.wheel(0, 400)
        await asyncio.sleep(0.8)
        s1 = await page.evaluate("window.scrollY")
        print(f"Scroll after wheel 1: {s1}")
        await page.screenshot(path="branding/verification/wheel_scroll_400.png")

        # 2. Scroll down another 1000px with wheel (into studio / features)
        print("2. Wheeling down 1000px...")
        await page.mouse.wheel(0, 1000)
        await asyncio.sleep(1.0)
        s2 = await page.evaluate("window.scrollY")
        print(f"Scroll after wheel 2: {s2}")
        await page.screenshot(path="branding/verification/wheel_scroll_1400.png")

        # 3. Scroll down another 1500px with wheel (into features / community)
        print("3. Wheeling down 1500px...")
        await page.mouse.wheel(0, 1500)
        await asyncio.sleep(1.2)
        s3 = await page.evaluate("window.scrollY")
        print(f"Scroll after wheel 3: {s3}")
        await page.screenshot(path="branding/verification/wheel_scroll_2900.png")

        # 4. Scroll all the way down to bottom / footer
        print("4. Wheeling down to footer...")
        await page.mouse.wheel(0, 3000)
        await asyncio.sleep(1.5)
        s4 = await page.evaluate("window.scrollY")
        print(f"Scroll after wheel 4 (footer): {s4}")
        await page.screenshot(path="branding/verification/wheel_scroll_footer.png")

        # 5. Scroll back up with wheel to 0
        print("5. Wheeling back up to top...")
        await page.mouse.wheel(0, -6000)
        await asyncio.sleep(1.5)
        s5 = await page.evaluate("window.scrollY")
        print(f"Scroll after wheeling back to top: {s5}")
        await page.screenshot(path="branding/verification/wheel_scroll_back_to_top.png")

        print("Total console errors:", len(console_errors))
        if len(console_errors) == 0:
            print("PERFECT: 0 console errors throughout entire mouse wheel playthrough!")

asyncio.run(main())
