from behave import step
from Pages.loginPages import loginPages as lp
from Pages.enquiryPages import enquiryPages as ep
from Pages.APIPages import APIPages 
from Pages.opportunityPages import opportunityPages as opp
from Pages.siteVisit import siteVisit as sv
from Pages.negotiationPage import negotiationPage as np
from support.shared_data import shared
import asyncio
#________________________________________API Login_____________________________________________________________

@step("go to salesforce and create the enquiry")
def step_impl(context):

    context.header = {
        "Authorization": f"Bearer {context.access_token}",
        "Content-Type": "application/json"
    }

    print("Token is ready for API calls")


@step("create enquiry record using API with '{name}' '{phone}' '{email}'")
def step_create_enquiry(context, name, phone, email):
    context.enquiry_name = name 

    context.api_page = APIPages(
        context.instance_url,
        context.header
    )

    context.api_page.create_enquiry(name, phone, email)

@step("enquiry should be created successfully")
def step_validate_enquiry(context):

    context.enquiry_id = context.api_page.validate_enquiry_created()

    
@step("store enquiry id")
def step_impl(context):

    shared["enquiry_id"] = context.enquiry_id
    shared["enquiry_name"] = context.enquiry_name
    print("Stored ID:", shared["enquiry_id"])
    print("SHARED DATA:", shared)
    print("Enquiry Name:", shared["enquiry_name"])


#______________________________________________UI Login ___________________________________________________

@step("login to the salesforce application using JWT")
def loginWithJWT(context):

    async def login():

        frontdoor_url = (
            f"{context.instance_url}"
            f"/secur/frontdoor.jsp?sid={context.access_token}"
        )

        print("Opening:", frontdoor_url)

        await context.page.set_viewport_size(
            {"width": 1400, "height": 900}
        )

        

        await context.page.goto(
            frontdoor_url,
            wait_until="domcontentloaded"
        )

        # ===== DEBUG START =====
        # await context.page.wait_for_load_state("domcontentloaded")
        # print("Current URL:", context.page.url)

        # try:
        #     await context.page.wait_for_selector(
        #         "button[title='App Launcher']",
        #         timeout=30000
        #     )
        #     print("Salesforce Lightning loaded")
        # except Exception as e:
        #     print("Lightning not loaded")
        #     print("Current URL:", context.page.url)
        #     print("Error:", str(e))

        #     await context.page.screenshot(
        #         path="login_failed.png",
        #         full_page=True
        #     )
        #     raise
        # ===== DEBUG END =====

        # ===== ORIGINAL CI CODE =====
        await context.page.wait_for_url(
            "**/lightning/**",
            timeout=120000
        )
        
        await context.page.wait_for_selector(
            "button[title='App Launcher']",
            timeout=120000
        )
        
        print("Login successful - UI loaded")
        
        print("Current URL:", context.page.url)
        await context.page.screenshot(
            path="sf_login.png",
            full_page=True
        )
        # ===== ORIGINAL CI CODE =====

    context.loop.run_until_complete(login())

@step("user should be navigate the enquiry created in API")
def step_impl(context):

     async def open_enquiry():

        enquiry_id = shared.get("enquiry_id")
        expected_name = shared.get("enquiry_name")  # ✔ from API

        print("Retrieved Enquiry ID:", enquiry_id)
        print("Expected Name from API:", expected_name)

        if not enquiry_id:
            raise Exception("Enquiry ID not found in shared data")

        record_url = (
            f"{context.instance_url}/lightning/r/"
            f"{enquiry_id}/view"
        )

        print("Opening Record:", record_url)

        await context.page.goto(record_url, wait_until="domcontentloaded")
        print("dom loaded")
        await context.page.wait_for_selector("h1 lightning-formatted-text",timeout=120000)
        

        title_locator = context.page.locator(
            "h1 lightning-formatted-text"
        )

        await title_locator.wait_for(state="visible", timeout=120000)

        actual_name = (await title_locator.text_content()).strip()

        print("UI Name:", actual_name)

        assert actual_name == expected_name, \
            f"Mismatch: UI={actual_name}, API={expected_name}"

        await context.page.screenshot(
            path="enquiry_record.png",
            full_page=True
        )
     context.loop.run_until_complete(open_enquiry())



@step("user should be navigate to the AWH application")
def navigateToAWH(context):
    context.ep = ep(context.page)
    context.loop.run_until_complete(context.ep.navigateToAWH())

@step("User needs to wait for 5mins to get the account created in salesforce")
def waitForAccountCreation(context):
    context.loop.run_until_complete(context.ep.waitTillAccountCreated(context.access_token,context.instance_url,shared.get("enquiry_id")))

@step("add the interested Location to the enquiry record and save it")
def addInterestedLocation(context):
    context.loop.run_until_complete(context.ep.addInterestedLocation())
    context.loop.run_until_complete(context.ep.EditInterestedLocation())

@step("Edit the enquiry and update the additional details")
def editAndUpdateEnquiry(context):
    context.loop.run_until_complete(context.ep.editEnquiryDetails())
    

@step("update the enquiry status to closed and qualified the enquiry")
def closeAndQualifyEnquiry(context):
    context.loop.run_until_complete(context.ep.ClosedEnquiry())

@step("Verify the user is successfully able to navigate to opportunity page")
def navigateToOpp(context):
    context.loop.run_until_complete(context.ep.navigateToOpp())

@step('verify the opportunity is in "{stagename}" stage')
def verifyStage(context, stagename):
    context.opp = opp(context.page)
    context.loop.run_until_complete(context.opp.verifyStages(stagename))

@step("go to the search unit tab and add the unit in the unit options")
def searchUnit(context):
    context.opp = opp(context.page)
    context.loop.run_until_complete(context.opp.searchUnit())

@step("click on the generate proposal and send the proposal to the customer")
def generateProposalPDF(context):
    context.opp = opp(context.page)
    context.loop.run_until_complete(context.opp.generateProposal())



@step("Click on the schedule site visit and create the site visit record")
def createSiteVisit(context):
    context.sv = sv(context.page)
    context.loop.run_until_complete(context.sv.createSiteVisit())


@step("navigate to the site visit record and update the site visit status")
def navigateTositeVisit(context):
    # context.sv = sv(context.page)
    context.loop.run_until_complete(context.sv.navigateToSiteVisit())

@step("Complete the site visit and back to Opportunity")
def markComplete(context):
    #  context.sv = sv(context.page)
     context.loop.run_until_complete(context.sv.markCompleteSV())
    #  asyncio.run(context.sv.markCompleteSV())

@step("Verify the user is successfully able to navigate to Opp from Site visit")
def OppfromSV(context):
    context.loop.run_until_complete(context.sv.navigativeToOppFromSV())

   
@step("generate the negotiation checklist and send to the customer")
def negoChecklist(context):
    context.np = np(context.page)
    context.loop.run_until_complete(context.np.negotiationCreation())



#__________________________________________________________________________________________________________________


@step("go to the salesforce test environment")
def navigateToSF(context):

    context.lp = lp(context.page)
    context.loop.run_until_complete(context.lp.goToSalesforce())


@step("verify the user is successfully able to login into the salesforce application")
def verifyLogin(context):
    try:
        context.loop.run_until_complete(context.lp.verifyLogin())

    except Exception as e:
        context.loop.run_until_complete(
            context.page.screenshot(
                path="failure.png",
                full_page=True
            )
        )
        print("📸 Screenshot captured in step")
        raise e





@step("click on the Enquiry tab and click on the New button")
def clickEnquiryTab(context):
    context.ep = ep(context.page)
    context.loop.run_until_complete(context.ep.clickEnquiryTab())

@step("fill the mandatory fields and click on the save button")
def fillMandatoryFields(context):
    context.loop.run_until_complete(context.ep.screen1())
    context.loop.run_until_complete(context.ep.screen2())
    context.loop.run_until_complete(context.ep.screen3())

@step("Go to the enquiry tab and verify the record is created")
def searchenquiry(context):
    context.ep = ep(context.page)
    context.loop.run_until_complete(context.ep.searchEnquiry())
    context.loop.run_until_complete(context.ep.verifyEnquiry())


@step("verify the enquiry is created successfully")
def verifyEnquiry(context):
    context.loop.run_until_complete(context.ep.verifyEnquiry())


@step("click on the edit and add the necessary fields to the enquiry")
def editEnquiry(context):
    context.loop.run_until_complete(context.ep.editEnquiry())

@step("go the Opportunity tabe and click on the opportunity record which is created from the enquiry record")
def clickOpportunity(context):
    context.opp = opp(context.page)
    context.loop.run_until_complete(context.opp.navigateToOpp())
    # context.loop.run_until_complete(context.opp.verifyOppRec())





