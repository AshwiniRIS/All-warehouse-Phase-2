async def safe_click(page, selector, text=None, role=None):
    try:
        print(f"Trying original locator: {selector}")
        await page.click(selector)
        return True

    except Exception as e:
        print("Primary locator failed:", e)

        if text:
            try:
                print(f"Trying text locator: {text}")
                await page.get_by_text(text).click()
                return True
            except Exception: 
                pass

        if role and text:
            try:
                print(f"Trying role locator: {role} with name {text}")
                await page.get_by_role(role, name=text).click()
                return True
            except Exception:
                pass

        print("All locator strategies failed")
        raise