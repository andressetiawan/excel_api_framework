Feature: Bank transfer
    Scenario Outline: System able to do payment using Virtual Account
        Given prepare request data for "<bank>" virtual account
        And set request authentication
        When send the request
        And do payment
        Then do payment check

        Examples:
            | bank    |
            | bca     |
            | bni     |
            | permata |