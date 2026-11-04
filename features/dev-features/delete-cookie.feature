@t010 @logout
Feature: Logout by deleting cookies
  As a customer I want my session to end when site data is deleted
  so that this browser no longer shows me as logged on

  Scenario: Logout by deleting Chrome cookies and site data
    Given the customer is logged out
    When the customer logs on by submitting the logon form
    Then the logon feedback page is My Account
    When the customer deletes cookies and site data in Chrome
    Then this site has no cookies stored
    When the customer reloads the page
    Then the old session cookie is gone
    And the page shows no logon sign
