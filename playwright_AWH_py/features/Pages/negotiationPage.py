from support.shared_data import shared
class negotiationPage:

    def __init__(self,page):
        self.page = page

    async def negotiationCreation(self):
        enquiry_name = shared.get("enquiry_name")
        print("Enquiry name :" ,enquiry_name)
        await self.page.get_by_role("button", name="Show more actions").click()
        await self.page.get_by_role("menuitem",name="Negotiation Checklist").click()
        print("NC is clicked")
        await self.page.locator("//select[@name='Select_a_Unit_Bundle']").click()
        await self.page.locator("//select[@name='Select_a_Unit_Bundle']").select_option(label="Option - 1")
        await self.page.locator("//input[@name='Save_Negotiation_Document_As']").fill(enquiry_name)
        await self.page.get_by_role("button", name="Next").click()
        save_button = self.page.get_by_role("button", name = "Save")
        await save_button.scroll_into_view_if_needed()
        await save_button.click()
