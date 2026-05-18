import os
import asyncio
import re
from playwright.async_api import async_playwright
# from util.SF_CONFIG import SF_CONFIG
# from Pages.APIPages import APIPages

STATE_FILE = "state.json"


def before_all(context):
    # context.base_URL = SF_CONFIG["instance-url"]
    # context.header = {
    #     "Authorization": f"Bearer {SF_CONFIG['access-token']}",
    #     "Content-Type": "application/json"
    # }
    # context.api_pages = APIPages(context.base_URL, context.header)
    pass

def before_scenario(context, scenario):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    context.loop = loop

    async def setup():
        context.playwright = await async_playwright().start()
        context.browser = await context.playwright.chromium.launch(
            headless=False,
            slow_mo=500
        )

        # ✅ Load state.json if it exists
        if os.path.exists(STATE_FILE):
            print("✅ Loading saved session from state.json")
            context.context = await context.browser.new_context(
                storage_state=STATE_FILE
            )
        else:
            print("⚠️  state.json not found — run: python save_session.py")
            raise FileNotFoundError(
                "state.json missing! Run 'python save_session.py' first."
            )

        context.page = await context.context.new_page()
        context.page.set_default_timeout(60000)

    context.loop.run_until_complete(setup())

def after_step(context, step):
    if step.status == "failed":
        os.makedirs("screenshots", exist_ok=True)
        async def take_screenshot():
            try:
                safe_name = re.sub(r'[\\/*?:"<>|]', "", step.name)
                await context.page.screenshot(
                    path=f"screenshots/{safe_name}.png",
                    full_page=True
                )
                print(f"📸 Screenshot saved: screenshots/{safe_name}.png")
            except Exception as e:
                print(f"⚠️  Screenshot failed: {e}")
        context.loop.run_until_complete(take_screenshot())

def after_scenario(context, scenario):
    async def teardown():
        try:
            if hasattr(context, "context"):
                await context.context.close()
        except Exception as e:
            print(f"⚠️  Context close: {e}")
        try:
            if hasattr(context, "browser"):
                await context.browser.close()
        except Exception as e:
            print(f"⚠️  Browser close: {e}")
        try:
            if hasattr(context, "playwright"):
                await context.playwright.stop()
        except Exception as e:
            print(f"⚠️  Playwright stop: {e}")

    context.loop.run_until_complete(teardown())
    context.loop.close()

def after_all(context):
    pass