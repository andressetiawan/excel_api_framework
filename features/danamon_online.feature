Feature: Danamon online
    Scenario: System able to do payment using danamon online
        Given prepare request data for danamon online payment
        And set request authentication
        When send danamon online payment request
        And do payment using danamon online
        Then do payment check
