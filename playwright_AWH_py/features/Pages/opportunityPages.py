from Pages.enquiryPages import enquiryPages
class opportunityPages:

    def __init__(self,page):
        self.page = page

    async def navigateToOpp(self):
        await self.page.get_by_title("Show Navigation Menu").click()
        await self.page.locator("//a[@role='menuitem' and @data-label='Opportunities']").click()
        await self.page.wait_for_timeout(10000) 
        await self.page.reload()
        searchButton =  self.page.get_by_label("Search this list...")
        await searchButton.click()
        await searchButton.fill(enquiryPages.enquiryName)
        await searchButton.press("Enter")
        print("search is able to use")
        await self.page.get_by_role("link", name=enquiryPages.enquiryName).first.click()
        
    async def verifyOppRec(self):
        await self.page.wait_for_timeout(10000) 
        name = await self.page.locator("h1 lightning-formatted-text").text_content()
        assert name == enquiryPages.enquiryName
        print("Opportunity is created successfully", name)

    async def verifyStages(self, stagename):
     stage_locator = self.page.locator(f"//a[@title='{stagename}']")
     await stage_locator.wait_for(state="visible", timeout=10000)
     actualStage = await stage_locator.text_content()
     actualStage = actualStage.strip()
     print("actual stage is", actualStage)
     assert actualStage == stagename
     print(f"Opportunity is in {stagename} stage")

        
    async def searchUnit(self):
        await self.page.get_by_role("tab",name="Search Units").click()
        await self.page.wait_for_timeout(5000)
        await self.page.get_by_placeholder("Enter Unit Number....").fill("test")
        await self.page.keyboard.press("Enter")
        await self.page.mouse.wheel(0, 1000)
        print("page scroll down")
        await self.page.wait_for_timeout(5000)
        checkbox = self.page.locator("//span[@class='slds-form-element__label']/preceding-sibling::span")
        count = await checkbox.count()
        print("number of checkbox is", count)
        if count == 3:
            select_count = 3
        elif count > 3:
            select_count = 4
        else:
            select_count = count    
        for i in range(select_count):
            await checkbox.nth(i).click()
            print(f"checkboc {i+1} is selected")
        await self.page.get_by_role('button', name="Add Unit").click()
        print("Add unit button is clicked")
        modal = self.page.locator("//lightning-formatted-rich-text//span//p")
        await modal.scroll_into_view_if_needed()
        await modal.wait_for(state="visible", timeout=1000)
        TextVisible = await modal.text_content()
        print("text visible in modal is", TextVisible)
        await self.page.locator("//header//button[@title='Close']").click()

    
    async def generateProposal(self):
        await self.page.get_by_role("button", name="Show more actions").click()
        await self.page.get_by_role("menuitem",name="Generate Proposal").click()
        print("generate proposal is clicked")
        checkbox = self.page.locator("//div[@class='quick-actions-panel']//label")
        count = await checkbox.count()
        print("number of checkbox is", count)
        if count == 5:
            select_count = 4
        elif count < 5:
            select_count = 3
        else:
            select_count = count
        for i in range(select_count):
            await checkbox.nth(i).scroll_into_view_if_needed()
            await checkbox.nth(i).click(force=True)
            print(f"checkbox {i+1} is selected in the pdf")
        await self.page.get_by_role("button", name="Next").click()
        print("Next button is clicked")
        await self.page.locator("//input[@name='clientName']").fill(enquiryPages.enquiryName)
        await self.page.locator("//input[@name='location']").fill("Parrys")
        await self.page.locator("//input[@name='size']").fill("1000")
        await self.page.get_by_role("button", name="Next").click()
        FileSection = self.page.locator("//c-file-organiser-header")
        await FileSection.scroll_into_view_if_needed()
        print("file section is visible")
        pdftext = enquiryPages.enquiryName +"_Parrys_1000.Pdf"
        await self.page.locator(f"//td[contains(text(),'{pdftext}')]").wait_for(state="visible", timeout=10000)
        print(pdftext, "is generated successfully")
        assert await self.page.locator(f"//td[contains(text(),'{pdftext}')]").is_visible() == True
        await self.page.get_by_role("button", name="Show more actions").click()
        await self.page.get_by_role("menuitem",name="Send Proposal to Customer").click()

    

       

       
        
        
