Feature: Search for pets by category

As a pet shop customer
I need to be able to search for a pet by category
So that I only see the category of pet I am interested in buying

Background:
    Given the following pets
        | name   | category | available |
        | Fluffy | cat      | true      |
        | Fido   | dog      | true      |
        | Polly  | bird     | true      |
        | Rover  | dog      | false     |
        | Jolly  | cat      | true      |
        | Molly  | dog      | true      |
        | Dolly  | bird     | true      |

Scenario: Search for pets by category
    Given I am a pet shop customer
    And I am on the "Home page"
    When I search for pets by "Category" "dog"
    And I click the "Search" button
    Then I should see the following pets
        | name  | category | available |
        | Fido  | dog      | true      |
        | Rover | dog      | false     |
        | Molly | dog      | true      |
    And I should see the message "3 pets found"
    And I should not see the following pets
        | name   | category | available |
        | Fluffy | cat      | true      |
        | Polly  | bird     | true      |
        | Jolly  | cat      | true      |
        | Dolly  | bird     | true      |
