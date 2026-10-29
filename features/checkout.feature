@checkout
Feature: Checkout
  As a shopper I want to place an order from my cart
  so that I can buy the products I chose

  Background:
    Given I am on the store home page
    When I add "Samsung galaxy s6" to the cart
    And I open the cart page

  Scenario: The order form shows the cart total
    When I click Place Order
    Then the order form total should equal the cart total

  Scenario: An empty order form is rejected
    When I click Place Order
    And I submit the order form
    Then I should see the alert "Please fill out Name and Creditcard."

  Scenario: An order without a card number is rejected
    When I click Place Order
    And I fill in only the name on the order form
    And I submit the order form
    Then I should see the alert "Please fill out Name and Creditcard."

  Scenario: An order without a name is rejected
    When I click Place Order
    And I fill in only the card number on the order form
    And I submit the order form
    Then I should see the alert "Please fill out Name and Creditcard."

  @order
  Scenario: A valid order is placed and the amount matches the cart
    When I click Place Order
    And I fill in valid details on the order form
    And I submit the order form
    Then I should see a purchase confirmation
    And the confirmation amount should equal the cart total

  @order
  Scenario: The cart is emptied after a purchase
    When I click Place Order
    And I fill in valid details on the order form
    And I submit the order form
    And I wait a bit
    And I accept the purchase confirmation
    And I open the cart page
    Then the cart should be empty
