import asyncio
from playwright.async_api import async_playwright

async def test_playwright():
    try:
        async with async_playwright() as p:
            print("Launching browser...")
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            print("Navigating to google.com...")
            await page.goto("https://www.google.com")
            title = await page.title()
            print(f"Page title: {title}")
            await browser.close()
            print("Playwright is working!")
    except Exception as e:
        print(f"Playwright error: {e}")

if __name__ == "__main__":
    asyncio.run(test_playwright())
