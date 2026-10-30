import asyncio, os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel='msedge')
        page = await browser.new_page(viewport={'width': 800, 'height': 600})
        abs_path = os.path.abspath('branding/zetica-monogram-black.svg').replace('\\', '/')
        await page.goto(f'file:///{abs_path}')
        os.makedirs('branding/verification', exist_ok=True)
        await page.screenshot(path='branding/verification/ze_black_svg_render.png')
        await browser.close()
        print('Captured branding/verification/ze_black_svg_render.png')

if __name__ == '__main__':
    asyncio.run(main())
