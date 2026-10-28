@cart
Feature: Shopping cart
  As a shopper I want to manage the items in my cart
  so that I only pay for what I actually want

  Scenario: A new visitor has an empty cart
    Given I have an empty cart
    When I open the cart page
    Then I should see the empty cart message

  @smoke
  Scenario: Add a single product to the cart
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    Then the cart should contain "iPhone" with quantity 1

  Scenario Outline: Line total reflects the quantity
    Given I have an empty cart
    When I add "iPhone" to the cart with quantity <qty>
    And I open the cart page
    Then the cart should contain "iPhone" with quantity <qty>
    And the line total for "iPhone" should be <qty> times the unit price

    Examples:
      | qty |
      | 1   |
      | 2   |
      | 5   |

  Scenario: Update the quantity of a product in the cart
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    And I update the quantity of "iPhone" to 3
    Then the cart should contain "iPhone" with quantity 3
    And the line total for "iPhone" should be 3 times the unit price

  Scenario: Remove the only product from the cart
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I open the cart page
    And I remove "iPhone" from the cart
    Then I should see the empty cart message

  Scenario: Cart sub-total adds up across different products
    Given I have an empty cart
    When I add "iPhone" to the cart
    And I add "Canon EOS 5D" to the cart with quantity 2
    And I open the cart page
    Then the cart should contain 2 line items
    And the cart sub-total should equal the sum of the line totals

  Scenario: Cart contents survive a page reload
    Given I have an empty cart
    When I add "Nikon D300" to the cart
    And I open the cart page
    And I reload the cart page
    Then the cart should contain "Nikon D300" with quantity 1
