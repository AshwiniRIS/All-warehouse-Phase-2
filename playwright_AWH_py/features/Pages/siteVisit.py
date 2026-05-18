from Pages.enquiryPages import enquiryPages
from datetime import datetime, timedelta
class siteVisit:

    def __init__(self,page):
        self.page = page

    async def createSiteVisit(self):
        future_date = (datetime.now() + timedelta(days=2)).strftime("%d-%b-%Y")
        await self.page.get_by_role("button",name="Schedule Site Visit").click()
        await self.page.wait_for_timeout(5000)
        await self.page.locator("//input[@name='Visit_Date']").nth(0).fill(future_date)
        print("future date is entered")
        await self.page.locator("//input[@name='Visit_Date']").nth(1).clear()
        await self.page.locator("//input[@name='Visit_Date']").nth(1).fill("3:45 pm")
        print("visit time is entered")
        await self.page.locator("//input[@name='No_of_People_Planned']").fill("3")
        await self.page.locator("//select[@name='Unit_Bundle']").click()
        await self.page.locator("//select[@name='Unit_Bundle']").select_option(label="Option - 1")
        print("unit bundle is selected")
        await self.page.get_by_role("button", name="Save").click()
        print("save button is clicked")
        await self.page.wait_for_timeout(5000)
        
        
