Feature: Salesforce login

@EnquiryPage
Scenario: Login to the salesforce application via API and create the enquiry record
  Given go to the salesforce test environment 
  Then give the username and password
  And Click on the Login button
  And verify the user is successfully able to login into the salesforce application
  Then click on the Enquiry tab and click on the New button
  And fill the mandatory fields and click on the save button
  Then Go to the enquiry tab and verify the record is created
  Then add the interested Location to the enquiry record and save it
  And click on the edit and add the necessary fields to the enquiry
  And Verify the user is successfully able to navigate to opportunity page
  

@OpportunityPage
Scenario: Login to the salesforce application and navigate to opprtunity page
  Given go to the salesforce test environment 
  Then give the username and password
  And Click on the Login button
  And verify the user is successfully able to login into the salesforce application
  Then go the Opportunity tabe and click on the opportunity record which is created from the enquiry record
  And verify the opportunity is in "Qualified" stage
  And go to the search unit tab and add the unit in the unit options
  Then click on the generate proposal and send the proposal to the customer
  And verify the opportunity is in "Proposal" stage

  @SiteVisitPage
  Scenario: Login to the salesforce application and navigate to sitevisit page
  Given go to the salesforce test environment 
  Then give the username and password
  And Click on the Login button
  And verify the user is successfully able to login into the salesforce application
  Then go the Opportunity tabe and click on the opportunity record which is created from the enquiry record
  And verify the opportunity is in "Proposal" stage
  And Click on the schedule site visit and create the site visit record
  # Then verify the site visit record is created successfully
  # And verify the opportunity is in "Site Visit " stage














# Then click on the Enquiry tab and click on the New button
  # And fill all the necessary fields and click on the save button
# And fill the mandatory fields and click on the save button
# And verify the enquiry is created successfully

  # Then add the interested location to the enquiry record and save it
  # Then Edit the enquiry and update the details and save the record
  # And Verify the user is successfully able to navigate to opportunity page

