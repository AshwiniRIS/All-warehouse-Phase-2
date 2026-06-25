Feature: Salesforce login

 @API
Scenario Outline: Create Enquiry via Salesforce API and perform the E2E flow in the SF application
    Given go to salesforce and create the enquiry
    When create enquiry record using API with '<name>' '<phone>' '<email>'
    Then enquiry should be created successfully
    And  store enquiry id

    Given login to the salesforce application using JWT
    # Then user should be navigate to the AWH application
    Then user should be navigate the enquiry created in API
    And User needs to wait for 5mins to get the account created in salesforce
    Then add the interested Location to the enquiry record and save it
    And Edit the enquiry and update the additional details
    Then update the enquiry status to closed and qualified the enquiry
    And Verify the user is successfully able to navigate to opportunity page
    # Then go the Opportunity tabe and click on the opportunity record which is created from the enquiry record
    And verify the opportunity is in "Qualified" stage
    And go to the search unit tab and add the unit in the unit options
    Then click on the generate proposal and send the proposal to the customer
    And verify the opportunity is in "Proposal" stage
    And Click on the schedule site visit and create the site visit record
    And verify the opportunity is in "Site Visit" stage
    Then navigate to the site visit record and update the site visit status
    And Complete the site visit and back to Opportunity
    And Verify the user is successfully able to navigate to Opp from Site visit
    Then generate the negotiation checklist and send to the customer
    And verify the opportunity is in "Negotiation" stage
    Examples:
    
      | name       | phone      | email                    |
      | Shiva     | 0999080896 | Shiva@2testgmail123.com |
  
















