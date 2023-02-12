Feature: Mandiri channel
    Scenario: System able to do payment using mandiri
        Given prepare request data for mandiri payment
        And set request authentication
        When send mandiri payment request
        And do payment using mandiri
        Then do payment check