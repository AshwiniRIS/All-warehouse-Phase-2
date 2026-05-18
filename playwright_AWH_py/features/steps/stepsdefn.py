from behave import step
from Pages.loginPages import loginPages as lp
from Pages.enquiryPages import enquiryPages as ep
from Pages.APIPages import APIPages as ap
from Pages.opportunityPages import opportunityPages as opp
from Pages.siteVisit import siteVisit as sv


@step("go to the salesforce test environment")
def navigateToSF(context):
    context.lp = lp(context.page)
    context.loop.run_until_complete(context.lp.goToSalesforce())


@step("give the username and password")
def enterCredentials(context):
    context.loop.run_until_complete(context.lp.enterUsername())
    context.loop.run_until_complete(context.lp.enterPassword())


@step("Click on the Login button")
def clickLoginButton(context):
    context.loop.run_until_complete(context.lp.clickLogin())


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

@step("add the interested Location to the enquiry record and save it")
def addInterestedLocation(context):
    context.loop.run_until_complete(context.ep.addInterestedLocation())
    context.loop.run_until_complete(context.ep.EditInterestedLocation())

@step("Edit the enquiry and update the details and save the record")
def editEnquiry(context):
    context.loop.run_until_complete(context.ep.editEnquiry())
  

@step("Verify the user is successfully able to navigate to opportunity page")
def navigateToOpp(context):
    context.loop.run_until_complete(context.ep.navigateToOpp())
    

@step("I have enquiry payload")
def createEnquiryPayload(context):
    pass

@step("I send create enquiry request")
def sendCreateEnquiryRequest(context):
    context.ap = ap(context.base_URL, context.header)
    payload = context.ap.create_enquiry()   
    context.enquiryName = payload["Name"]

@step("enquiry should be created successfully")
def verifyEnquiryCreated(context):
    context.ap.validate_enquiry_created()

@step("click on the edit and add the necessary fields to the enquiry")
def editEnquiry(context):
    context.loop.run_until_complete(context.ep.editEnquiry())

@step("go the Opportunity tabe and click on the opportunity record which is created from the enquiry record")
def clickOpportunity(context):
    context.opp = opp(context.page)
    context.loop.run_until_complete(context.opp.navigateToOpp())
    context.loop.run_until_complete(context.opp.verifyOppRec())

@step('verify the opportunity is in "{stagename}" stage')
def verifyStage(context, stagename):
    context.loop.run_until_complete(context.opp.verifyStages(stagename))

@step("go to the search unit tab and add the unit in the unit options")
def searchUnit(context):
    context.loop.run_until_complete(context.opp.searchUnit())

@step("click on the generate proposal and send the proposal to the customer")
def generateProposalPDF(context):
    context.loop.run_until_complete(context.opp.generateProposal())

@step("Click on the schedule site visit and create the site visit record")
def createSiteVisit(context):
    context.sv = sv(context.page)
    context.loop.run_until_complete(context.sv.createSiteVisit())
