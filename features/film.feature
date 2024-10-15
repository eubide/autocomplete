Feature: Film management

  Scenario: Add a film to the list
    Given I have an empty film list
    When I add "Inception" to the film list
    Then the film list should contain "Inception"