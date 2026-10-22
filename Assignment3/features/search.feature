Feature: Product search
  As a shopper I want to search the catalogue so I can find products quickly

  Background:
    Given I am on the store home page

  Scenario: Search for an existing product
    When I search for "iPhone"
    Then I should see search results
    And the results should include "iPhone"

  Scenario Outline: Search by different terms
    When I search for "<term>"
    Then I should see search results

    Examples:
      | term   |
      | Canon  |
      | Apple  |

  Scenario: Search with no matches
    When I search for "zzzzzz-no-match"
    Then I should see a "no product" message