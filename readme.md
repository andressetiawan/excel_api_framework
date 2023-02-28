# API Test Framework

## Pre-requisite:
- Download [test scenario template](https://docs.google.com/spreadsheets/d/1-igF1L6YWrHBjP5fzSt-bScvwn0LT0uP1M_mbLNvauE/edit?usp=sharing) for this framework
- Python 3.10.x or above
- pip 22.x.x or above
- NPM 9.x or above

#### Run this code
```sh
pip install behave

sh install.sh
```

## How ro run test?
Run this code
```sh
sh test.sh <test_scenario_file>
```

## Test case documentation
Build-in variables in Request body:
| Variables | Description | Example | Result |
| --------- | ----------- | ------- | ------ |
| {{$uuid}} | Generate random UUID | { "customer_id" : {{$uuid}} } | { "customer_id" : 1234567890 }

Query data for API URL:
| API URL | Example query data | Result |
| ------- | ------------------ | ------ |
| `https://test.com/{{id}}` | { "id":"001" } | https://test.com/001
| `https://test.com?id={{id}}` | { "id":"001" } | https://test.com?id=001
| `https://test.com?id={{id}}&name={{name}}` | { "id" : "001", "name" : "test" } | https://test.com?id=001&name=test
| `https://test.com/id/{{id}}/name/{{name}}` | { "id" : "001", "name" : "test" } | https://test.com/id/001/name/test |