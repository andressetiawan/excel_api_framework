Feature: REST API Automation
    Scenario: Run REST API automation framework
    Given Prepare testing request data and headers
    When Client send request data
    Then System checks json schema
    And System generate report