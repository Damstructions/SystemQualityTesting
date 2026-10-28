@auth
Feature: Sign up and log in
  As a shopper I want an account
  so that I can log in to the store

  Background:
    Given I am on the store home page

  Scenario: Register a new account
    When I sign up with a new username
    Then I should see the alert "Sign up successful."

  @smoke
  Scenario: Log in after registering
    When I sign up with a new username
    And I log in with that username and password
    Then I should see the welcome message for that user

  Scenario: Log in with the wrong password
    When I sign up with a new username
    And I log in with that username and the wrong password
    Then I should see the alert "Wrong password."

  Scenario: Log in with an unknown user
    When I log in as the unknown user "no_such_user_qa_12345"
    Then I should see the alert "User does not exist."
