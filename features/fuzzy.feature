Feature: Fuzzy Autocomplete

  Scenario: Add items and get the one
    Given a Redis client
    And an empty Redis database
    When I add the following items to the autocomplete system:
      | item     |
      | apple    |
      | banana   |
      | cherry   |
      | date     |
      | fig      |
      | grape    |
      | hello    |
      | helium   |
      | hero     |
      | helicopter|
    And I get fuzzy suggestions for "helo"
    Then the suggestions should contain some of the following:
      | suggestion |
      | hello      |
      | hero       |



  Scenario: Add items and get a list of fuzzy suggestions
    Given a Redis client
    And an empty Redis database
    When I add the following items to the autocomplete system:
      | item     |
      | apple    |
      | banana   |
      | cherry   |
      | date     |
      | fig      |
      | grape    |
      | hello    |
      | helium   |
      | hero     |
      | helicopter|
    And I get fuzzy suggestions for "helo"
    Then the first suggestion should be "hello"