@t010 @logout
Feature: User logout
  As a customer I want to log out from My Account
  so that the store shows I have logged off

  Scenario: Logout after logon using the My Account button
    Given the customer is logged out
    When the customer logs on by submitting the logon form
    Then the logon feedback page is My Account
    When the customer clicks the Logout button in My Account
    Then the logout feedback page is shown
