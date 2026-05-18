import asyncio
from playwright.async_api import async_playwright

STATE_FILE = "state.json"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        context = await browser.new_context()
        page = await context.new_page()

        # Open Salesforce login page
        await page.goto("https://test.salesforce.com")

        print("Login manually in browser...")
        input("After login press ENTER here...")

        # Save login session
        await context.storage_state(path=STATE_FILE)

        print("✅ state.json created successfully")

        await browser.close()

asyncio.run(main())