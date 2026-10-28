@cart
Feature: Shopping cart
  As a shopper I want to manage the items in my cart
  so that I only pay for what I want

  Background:
    Given I am on the store home page

  Scenario: A new visitor has an empty cart
    When I open the cart page
    Then the cart should be empty

  @smoke
  Scenario: Add a product to the cart
    When I add "Samsung galaxy s6" to the cart
    And I open the cart page
    Then the cart should contain "Samsung galaxy s6"
    And the number of cart lines should be 1
    And the cart total should equal the sum of the item prices

  Scenario Outline: The cart price matches the product page price
    When I add "<product>" to the cart
    And I open the cart page
    Then the cart price for "<product>" should match its product page price

    Examples:
      | product           |
      | Samsung galaxy s6 |
      | Nokia lumia 1520  |
      | Sony vaio i5      |

  Scenario: Add two different products
    When I add "Samsung galaxy s6" to the cart
    And I add "Nexus 6" to the cart
    And I open the cart page
    Then the number of cart lines should be 2
    And the cart total should equal the sum of the item prices

  Scenario: Adding the same product twice creates two lines
    When I add "Nexus 6" to the cart 2 times
    And I open the cart page
    Then the number of cart lines should be 2
    And the cart total should be twice the price of "Nexus 6"

  Scenario: Remove one of two products
    When I add "Samsung galaxy s6" to the cart
    And I add "Nexus 6" to the cart
    And I open the cart page
    And I delete "Nexus 6" from the cart
    Then the cart should contain "Samsung galaxy s6"
    And the cart should not contain "Nexus 6"
    And the cart total should equal the sum of the item prices

  Scenario: Remove the only product
    When I add "Nokia lumia 1520" to the cart
    And I open the cart page
    And I delete "Nokia lumia 1520" from the cart
    Then the cart should be empty

  Scenario: Cart contents survive a page reload
    When I add "Sony vaio i5" to the cart
    And I open the cart page
    And I reload the cart page
    Then the cart should contain "Sony vaio i5"
