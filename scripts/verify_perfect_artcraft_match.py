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

        # 1. Dark Mode at Scroll 0
        print("1. Capturing Dark Mode at Scroll 0...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        """)
        await asyncio.sleep(1)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_0.png")

        # Check Hero Wordmark has NO logo
        hero_check = await page.evaluate("""() => {
            const masthead = document.getElementById('hero-wordmark-masthead');
            const letters = Array.from(document.querySelectorAll('#hero-wordmark-masthead .wm-letter'));
            const imgs = masthead ? masthead.querySelectorAll('img') : [];
            const flowLetters = Array.from(document.querySelectorAll('.flow-letter'));
            const flowSpans = flowLetters.map(el => ({
                text: el.textContent,
                fontSize: window.getComputedStyle(el).fontSize,
                transform: el.style.transform,
                opacity: el.style.opacity,
                color: el.style.color
            }));
            return {
                mastheadExists: !!masthead,
                letterCount: letters.length,
                letterChars: letters.map(l => l.textContent.trim()),
                inlineImagesInMasthead: imgs.length,
                flowLettersCount: flowLetters.length,
                sampleFlowSpans: flowSpans.slice(0, 5)
            };
        }""")
        print("Hero Masthead Check:", hero_check)

        # 2. Light Mode at Scroll 0
        print("2. Capturing Light Mode at Scroll 0...")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('light');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
            }
        """)
        await asyncio.sleep(1)
        await page.screenshot(path="branding/verification/perfect_light_scroll_0.png")

        # 3. Switch back to Dark Mode and test Scroll 500
        await page.evaluate("window.zeticaApplyTheme('dark')")
        print("3. Scrolling to 500px...")
        await page.evaluate("window.scrollTo(0, 500)")
        await asyncio.sleep(1)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_500.png")

        # 4. Scroll to 1500px (Studio / Features)
        print("4. Scrolling to 1500px...")
        await page.evaluate("window.scrollTo(0, 1500)")
        await asyncio.sleep(1)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_1500.png")

        # Inspect sidebar stack at 1500px
        stack_info = await page.evaluate("""() => {
            const heroLetters = Array.from(document.querySelectorAll('#hero-wordmark-masthead .wm-letter')).map(el => {
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                return {
                    char: el.textContent.trim(),
                    x: r.x,
                    y: r.y,
                    w: r.width,
                    h: r.height,
                    fontSize: cs.fontSize,
                    transform: el.style.transform,
                    opacity: el.style.opacity,
                    color: el.style.color
                };
            });

            const flowSpans = Array.from(document.querySelectorAll('.flow-letter')).map(el => {
                const r = el.getBoundingClientRect();
                const cs = window.getComputedStyle(el);
                return {
                    char: el.textContent.trim(),
                    x: r.x,
                    y: r.y,
                    w: r.width,
                    h: r.height,
                    fontSize: cs.fontSize,
                    transform: el.style.transform,
                    opacity: el.style.opacity,
                    color: el.style.color
                };
            }).filter(s => s.w > 0 && s.h > 0);

            return { heroLetters, flowSpans: flowSpans.slice(0, 25) };
        }""")
        print("\n--- Stack Info at Scroll 1500px ---")
        print("Hero ZETICA letters in stack:")
        for hl in stack_info['heroLetters']:
            print(f"  '{hl['char']}' => rect: ({hl['x']:.1f}, {hl['y']:.1f}, {hl['w']:.1f}x{hl['h']:.1f}) | font: {hl['fontSize']} | transform: {hl['transform']}")

        print("\nFlow Letters in stack / queue:")
        for fl in stack_info['flowSpans'][:15]:
            print(f"  '{fl['char']}' => rect: ({fl['x']:.1f}, {fl['y']:.1f}, {fl['w']:.1f}x{fl['h']:.1f}) | font: {fl['fontSize']} | transform: {fl['transform']}")

        # 5. Scroll to 3500px
        print("5. Scrolling to 3500px...")
        await page.evaluate("window.scrollTo(0, 3500)")
        await asyncio.sleep(1)
        await page.screenshot(path="branding/verification/perfect_dark_scroll_3500.png")

        print("\nConsole Errors Encountered:", console_errors)
        if len(console_errors) == 0:
            print("SUCCESS: 0 console errors detected!")
        else:
            print(f"WARNING: {len(console_errors)} console errors found!")

asyncio.run(main())
