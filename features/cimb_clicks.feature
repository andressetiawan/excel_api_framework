Feature: CIMB Clicks
    Scenario: System able to do payment using CIMB Clicks
        Given prepare request data for CIMB Clicks
        And set request authentication
        When send CIMB Clicks request
        And do payment using CIMB Clicks
        Then do payment check
