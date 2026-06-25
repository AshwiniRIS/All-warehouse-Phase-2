from Pages.enquiryPages import enquiryPages
from datetime import datetime, timedelta
from support.shared_data import shared
from playwright.async_api import expect
class siteVisit:


    def __init__(self,page):
        self.page = page
        self.site_visit_name = None
        print("site visit is initiated")

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
        await self.page.get_by_placeholder("Search People...").click()
        await self.page.locator("//span[@title='Pooja Bagri']").click()
        print("User is selected")
        await self.page.get_by_role("button", name="Save").click()
        print("save button is clicked")
        await self.page.wait_for_timeout(10000)
        enquiry_name = shared.get("enquiry_name")
        Convert_future_date = datetime.strptime(future_date, "%d-%b-%Y")
        future_date_sf = Convert_future_date.strftime("%d-%m-%Y")
        site_visit_name = f"{enquiry_name}-{future_date_sf}"
        self.site_visit_name = site_visit_name   # string
        shared["site_visit_name"] = site_visit_name
        site_visit_locator = self.page.locator(f"//a[contains(text(),'{site_visit_name}')]")
        await expect(site_visit_locator).to_be_visible()
        print("Site visit is created successfully:", site_visit_name)
    

    
    async def navigateToSiteVisit(self):
        site_visit_name = shared.get("site_visit_name")
        print("Retrieved:", site_visit_name)
        SiteVisit_locator = self.page.locator(f"//a[contains(text(),'{site_visit_name}')]")
        await SiteVisit_locator.click(force=True)
        # Navigate_SV =  self.site_visit_name 
        # print("Navigate to site visit", Navigate_SV)
        # SiteVisit_locator = self.page.locator(f"//a[contains(text(),'{Navigate_SV}')]")
        # await SiteVisit_locator.click(force=True)
        print("navigate to Sitevisit")
        # sv_loc = self.page.locator("//a[contains(text(),'Anish test-21-06-2026')]")
        # await sv_loc.click(force=True)
        await self.page.wait_for_timeout(10000)
        locator = self.page.locator("//*[contains(@class,'entityNameTitle') and contains(.,'Site Visit')]")
        await locator.wait_for(state="visible", timeout=15000)
        site_visit_name = await locator.inner_text()
        print("SITE VISIT TEXT:", site_visit_name, flush=True)
        assert "Site Visit" in site_visit_name

    async def markCompleteSV(self):
        print("1 mark button is clicked")
        markComplete_btn =  self.page.locator("//button[@name='Site_Visit__c.Mark_Complete']")
        await markComplete_btn.click()
        print("mark button is clicked")
        await self.page.get_by_role("button",name="Next").click()
        await self.page.get_by_role("button",name="Next").click()
        await self.page.wait_for_timeout(20000)
        Expected_text = 'Completed'
        acutal_text = await self.page.locator("//lightning-formatted-text[contains(text(),'Completed')]").text_content()
        print("Actual text = ",acutal_text)
        assert Expected_text == acutal_text
        print("Site visit is completed")
        opp_link = self.page.locator("//div[@data-target-selection-name='sfdc:RecordField.Site_Visit__c.Opportunity__c']//a")
        await opp_link.click()
        await self.page.wait_for_timeout(10000)
        print("navigate to Opp page")

    async def navigativeToOppFromSV(self):
        await self.page.wait_for_timeout(5000) 
        Opp = await self.page.locator("records-entity-label",  has_text="Opportunities").text_content()
        assert Opp == "Opportunities"
        print("user is successfully navigated to opportunity page", Opp)
    #    enquiry_name = shared.get("enquiry_name")
    #    Oppname =await self.page.locator("h1 lightning-formatted-text", has_text=enquiry_name).nth(1).text_content()
    #    assert Oppname == enquiry_name
        print("opportunity is created successfully", Opp)
        

    







        


    

        
