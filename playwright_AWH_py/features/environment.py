import asyncio
from multiprocessing import context
import os
import re

from playwright.async_api import async_playwright
from jwt_auth import get_access_token
from Pages.loginPages import loginPages as lp
from Pages.enquiryPages import enquiryPages as ep

def before_all(context):

    # Generate JWT token once
  access_token, instance_url, frontdoor_url = get_access_token()

  context.access_token = access_token
  context.instance_url = instance_url
  context.frontdoor_url = frontdoor_url

  print("✅ JWT Token Generated")
  print("✅ Instance URL:", instance_url)
  print("✅ Frontdoor URL:", frontdoor_url)


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

        context.context = await context.browser.new_context()

        context.page = await context.context.new_page()
        context.lp = lp(context.page)
        context.ep = ep(context.page)

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
                print(f"Screenshot Error: {e}")

        context.loop.run_until_complete(take_screenshot())


def after_scenario(context, scenario):

    async def teardown():

        if hasattr(context, "context"):
            await context.context.close()

        if hasattr(context, "browser"):
            await context.browser.close()

        if hasattr(context, "playwright"):
            await context.playwright.stop()

    context.loop.run_until_complete(teardown())
    context.loop.close()


def after_all(context):
    pass