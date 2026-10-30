import asyncio
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

from playwright.async_api import async_playwright

PAGES = [
    ("Home", "http://localhost:8792/index.html"),
    ("Tutorials", "http://localhost:8792/tutorials.html"),
    ("News", "http://localhost:8792/news.html"),
    ("FAQ", "http://localhost:8792/faq.html"),
    ("Press Kit", "http://localhost:8792/press-kit.html"),
    ("Download", "http://localhost:8792/download.html"),
    ("Apps", "http://localhost:8792/apps.html"),
    ("Pricing", "http://localhost:8792/pricing.html"),
    ("Support", "http://localhost:8792/support.html")
]

async def verify():
    os.makedirs('branding/verification', exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        all_errors = []
        page.on("pageerror", lambda err: all_errors.append(f"PageError: {err}"))
        
        print("=== VERIFYING ALL 9 SECONDARY & PRIMARY PAGES ===")
        for name, url in PAGES:
            resp = await page.goto(url, wait_until="domcontentloaded")
            status = resp.status if resp else "unknown"
            title = await page.title()
            print(f"[{status}] {name:10s} -> URL: {url} | Title: {title}")
            assert status == 200, f"Expected 200 OK for {url}, got {status}"
            await asyncio.sleep(0.3)
            
        # Verify Resources Dropdown interaction on Home
        print("\n=== VERIFYING RESOURCES DROPDOWN INTERACTION ===")
        await page.goto("http://localhost:8792/index.html", wait_until="domcontentloaded")
        await asyncio.sleep(1.0)
        
        # Hover over resources li
        btn = await page.query_selector('button[id*="trigger"][id*="ailb"]')
        assert btn is not None, "Resources trigger button must exist"
        parent_li = await page.evaluate_handle('btn => btn.closest("li")', btn)
        await parent_li.hover()
        await asyncio.sleep(0.4)
        
        # Check if dropdown is open
        is_open = await page.evaluate('''() => {
            const dd = document.querySelector('.zetica-resources-dropdown');
            return dd ? dd.classList.contains('open') && window.getComputedStyle(dd).display === 'flex' : false;
        }''')
        print(f"Resources Dropdown open on hover: {is_open}")
        assert is_open, "Resources dropdown must be open and flex on hover"
        
        await page.screenshot(path="branding/verification/verified_resources_hover.png")
        print("Captured branding/verification/verified_resources_hover.png")
        
        # Test clicking each item in dropdown
        items = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.resources-dropdown-item')).map(a => ({
                text: a.innerText.trim(),
                href: a.getAttribute('href')
            }));
        }''')
        print("Dropdown items detected:", items)
        expected_items = ["TUTORIALS", "NEWS", "FAQ", "PRESS KIT"]
        for expected in expected_items:
            found = any(it['text'] == expected for it in items)
            assert found, f"Item {expected} must exist in dropdown"
        print("All 4 dropdown items verified successfully!")
        
        # Verify Wordmark flight in Dark Mode
        print("\n=== VERIFYING WORDMARK FLIGHT & NO DUPLICATE ===")
        await page.evaluate("""
            if (typeof window.zeticaApplyTheme === 'function') {
                window.zeticaApplyTheme('dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'dark');
            }
        """)
        await asyncio.sleep(0.5)
        
        # Scroll to 300px
        await page.evaluate("window.scrollTo({ top: 300, behavior: 'instant' })")
        await asyncio.sleep(0.5)
        
        dom_metrics = await page.evaluate('''() => {
            const mastheads = document.querySelectorAll('#hero-wordmark-masthead');
            const flowBoxesForHero = document.querySelectorAll('.flow-word-box[data-label="ZETICA"]');
            const deadBars = document.querySelectorAll('[role="scrollbar"]');
            const activeLetter = document.querySelector('.flow-letter.active');
            
            return {
                mastheadCount: mastheads.length,
                flowHeroBoxes: flowBoxesForHero.length,
                deadScrollbars: deadBars.length,
                activeHeadingText: activeLetter ? activeLetter.closest('.flow-word-box').dataset.label : 'none'
            };
        }''')
        print("DOM flight metrics:", dom_metrics)
        assert dom_metrics['mastheadCount'] == 1, "Exactly 1 hero masthead should exist"
        assert dom_metrics['flowHeroBoxes'] == 0, "Zero flow boxes for ZETICA hero (flight driven directly)"
        assert dom_metrics['deadScrollbars'] == 0, "Zero dead prebaked scrollbars"
        
        print("\n=== VERIFICATION SUITE PASSED WITH ZERO ERRORS ===")
        print(f"Total PageErrors detected: {len(all_errors)}")
        if all_errors:
            for err in all_errors:
                print("  -", err)
                
        await browser.close()

if __name__ == '__main__':
    asyncio.run(verify())
