Feature: Virtual Account
    Scenario: System able to do payment using Permata Virtual Account
        Given prepare request data
        And set request authentication
        When send the request
        And do payment
        Then do payment check