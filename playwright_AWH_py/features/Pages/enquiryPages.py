from ai.healer import safe_click
class enquiryPages:

  enquiryName ="Test enquiry 7"

  def __init__(self,page):
    self.page = page

  async def clickEnquiryTab(self):
    try:
        await self.page.wait_for_timeout(20000)
        await self.page.get_by_title("All Warehouses").wait_for(timeout=10000)
        await self.page.get_by_title("Show Navigation Menu").click()
        await self.page.locator("//a[@role='menuitem' and @data-label='Enquiries']").click()
        print("enquiry tab is clicked")
        await self.page.get_by_role("button", name="New").click()
        print("new button is clicked")
    except Exception as e:
        await self.page.screenshot(path="debug_enquiry_error.png", full_page=True)
        raise e


  async def screen1(self):
    await self.page.get_by_placeholder("Enter Mobile Number").fill("2345654544")
    print("mobile number is entered")
    await self.page.get_by_placeholder("you@example.com").fill("xyz@ywe.com")
    print("email is entered")
    await self.page.get_by_role("button", name="Next").click()
    print("next button is clicked")

  async def screen2(self):
    await self.page.locator("//input[@name='lastName']").fill(enquiryPages.enquiryName)
    print("last name is entered")
    await self.page.get_by_role("button", name="Save").click()
    print("save button is clicked")
    await self.page.select_option('[name="Intent_Type"]', label="Tenant")
    print("intent type is selected")
    await self.page.get_by_role("button", name="Next").click()

  async  def screen3(self):
    await self.page.fill('[name="Budget_Range1__c"]', "45000")
    print("budget range is entered")
    await self.page.fill('[name="Size_in_sqfts__c"]',"2000")
    print("size in sqfts is entered")
    await self.page.get_by_role("combobox", name="Nature of Purchase").click()
    await self.page.get_by_role("option", name="Rent").click()
    print("nature of purchase is selected")
    await self.page.get_by_role("combobox", name="Service Required").click()
    await self.page.get_by_role("option", name="Shed").click()
    print("service required is selected")
    await self.page.get_by_role("combobox", name="Enquiry Source").click()
    await self.page.get_by_role("option", name="Offline").click()
    print("enquiry source is selected")
    await self.page.get_by_role("combobox", name="Enquiry Sub Source").click()
    await self.page.get_by_role("option", name="Walk-in").click()
    print("enquiry sub source is selected")
    await self.page.get_by_role("button", name="Next").click()
    await self.page.wait_for_timeout(5000)
    

  async def verifyEnquiry(self):
    name = await self.page.locator("h1 lightning-formatted-text").text_content()
    assert name == enquiryPages.enquiryName
    print("enquiry is created successfully", name)

  
  async def searchEnquiry(self):
   await safe_click(self.page,"[title='Enquiries']",text="Enquiries",role="listitem")
   print("enquiry tab is clicked")
   await self.page.wait_for_timeout(10000) 
   await self.page.reload()
   await self.page.wait_for_timeout(10000) 
   searchButton =  self.page.get_by_label("Search this list...")
   await searchButton.click()
   await searchButton.fill(enquiryPages.enquiryName)
   await searchButton.press("Enter")
   print("search is able to use")
   await self.page.get_by_role("link", name=enquiryPages.enquiryName).first.click()


  async def addInterestedLocation(self):

    # Step 1: Locate the middle scrollable column using your XPath
    scroll_area = self.page.locator(
        "//flexipage-record-home-scrollable-column[@class='col main-col slds-col']"
    ).first

    await scroll_area.wait_for(state="visible", timeout=10000)

    print("Scroll area found")

    # Step 2: Scroll inside the column until Interested Locations section appears
    for _ in range(8):

        await scroll_area.evaluate("""
        el => {
            el.scrollTop += 1000;
        }
        """)

        await self.page.wait_for_timeout(1000)

        # Check whether section appeared
        if await self.page.locator("text=Interested Locations").count() > 0:
            print("Interested Locations section found")
            break

    # Step 3: Wait for Interested Locations section
    section = self.page.locator("text=Interested Locations").first
    await section.wait_for(state="visible", timeout=20000)

    print("Section visible")

    # Step 4: Click New button inside Interested Locations related list
    new_btn = self.page.locator(
        "//span[normalize-space()='Interested Locations']"
        "/ancestor::article[contains(@class,'slds-card')]"
        "//button[@name='New']"
    )

    await new_btn.wait_for(state="visible", timeout=20000)
    await new_btn.click()

    print("Clicked Interested Locations New button")
  

  async def EditInterestedLocation(self):
    await self.page.get_by_label("Interested Locations Name").fill("Parrys")
    print("interested location name is entered")
    await self.page.get_by_label("Interested Location Range").fill("25")
    print("interested location range is entered")
    await self.page.locator("//button[@name='SaveEdit']").click()
    print("save button is clicked")
    enquiry_link = self.page.locator(f"(//a[@title='{enquiryPages.enquiryName} | Enquiry'])[2]")
    await enquiry_link.wait_for(state="visible", timeout=20000)
    await enquiry_link.click()
    print("Enquiry record opened")

  async def editEnquiry(self):

    # Locate the scrollable main column
    scrollable = self.page.locator(
        "//flexipage-record-home-scrollable-column[@class='col main-col slds-col']"
    ).first

    await scrollable.wait_for(state="visible", timeout=10000)

    # Scroll completely to top
    await scrollable.evaluate("""
        el => {
            el.scrollTop = 0;
        }
    """)

    print("Scrolled to top")

    # Click Edit button
    await self.page.locator("//button[@name='Edit']").click()
    print("edit button is clicked")

    # Update Size Range
    await self.page.get_by_role("combobox", name="Size Range").click()
    await self.page.get_by_role("option", name="below 10000").click()
    print("size range is updated")

    # Update Status
    await self.page.get_by_role("combobox", name="Status").click()
    await self.page.get_by_role("option", name="Closed").click()
    print("status is updated")

    # Update Reason for Closed
    await self.page.get_by_role("combobox", name="Reason for Closed").click()
    await self.page.get_by_role("option", name="Qualified", exact=True).click()
    print("reason for closed is updated")

    # Save
    await self.page.locator("//button[@name='SaveEdit']").click()
    print("save button is clicked")
   

  async def navigateToOpp(self):
    await self.page.get_by_role("button", name="Submit").click()
    print("submit button is clicked")
    await self.page.wait_for_timeout(5000) 
    Opp = await self.page.locator("records-entity-label",  has_text="Opportunities").text_content()
    assert Opp == "Opportunities"
    print("user is successfully navigated to opportunity page", Opp)
    Oppname =await self.page.locator("h1 lightning-formatted-text", has_text=enquiryPages.enquiryName).nth(1).text_content()
    assert Oppname == enquiryPages.enquiryName
    print("opportunity is created successfully", Oppname, Opp)


  async def editEnquiryDetails(self):
    await self.page.get_by_role("button", name="Change Record Type").click()
    print("change record type button is clicked")

    await self.page.locator("//span[@class='slds-form-element__label' and contains(text(),'Tenant')]").click()
    await self.page.get_by_role("button",name="Next").click()
    print("next button is clicked")
 
    await self.page.fill('[name="Budget_Range1__c"]', "45000")
    print("budget range is entered")

    await self.page.get_by_role("combobox", name="Nature of Purchase").click()
    await self.page.get_by_role("option", name="Rent").click()
    print("nature of purchase is selected")

    await self.page.get_by_role("combobox", name="Size Range").click()
    await self.page.get_by_role("option",name="below 10000").click()
    print("size range is updated")

    await self.page.get_by_role("combobox", name="Service Required").click()
    await self.page.get_by_role("option", name="Shed").click()
    print("service required is selected")

    await self.page.get_by_role("combobox", name="Enquiry Source").click()
    await self.page.get_by_role("option", name="Offline").click()
    print("enquiry source is selected")

    await self.page.get_by_role("combobox", name="Enquiry Sub Source").click()
    await self.page.get_by_role("option", name="Walk-in").click()
    print("enquiry sub source is selected")

    await self.page.locator("//button[@name='SaveEdit']").click()
    print("save button is clicked")
    








