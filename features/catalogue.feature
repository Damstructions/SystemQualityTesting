@catalogue
Feature: Product catalogue
  As a shopper I want to browse the catalogue
  so that I can find a product to buy

  Background:
    Given I am on the store home page

  @smoke
  Scenario: The home page lists products
    Then I should see products

  Scenario Outline: Browse products by category
    When I select the "<category>" category
    Then I should see products
    And the products should include "<product>"

    Examples:
      | category | product           |
      | Phones   | Samsung galaxy s6 |
      | Laptops  | MacBook air       |
      | Monitors | Apple monitor 24  |

  Scenario: Open a product page
    When I open the product "Samsung galaxy s6"
    Then the product page should show the name "Samsung galaxy s6"
    And the product page should show a price

  Scenario: The next page shows different products
    When I go to the next page of products
    Then I should see products
