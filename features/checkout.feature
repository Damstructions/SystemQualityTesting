@checkout
Feature: Checkout
  As a shopper I want to check out as a guest
  so that I can buy products without creating an account

  Scenario: Checkout with an empty cart is not possible
    Given I have an empty cart
    When I go directly to the checkout page
    Then I should be redirected to the cart page

  @smoke
  Scenario: Proceed from the cart to the checkout page
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    And I proceed to checkout from the cart
    Then I should be on the checkout page

  Scenario: Guest checkout rejects an empty billing form
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    And I proceed to checkout from the cart
    And I choose guest checkout
    And I continue without entering any details
    Then I should see validation errors

  @order @slow
  Scenario: Guest checkout places an order
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    And I proceed to checkout from the cart
    And I choose guest checkout
    And I enter valid guest billing details
    And I accept the terms and continue to confirmation
    And I confirm the order
    Then the order should be placed
