import requests
import json

class Validation:
    code: int = None

    def response(keys:str=""):
        result = Rest.response["response"]
        if(len(keys) > 0):
            keys = keys.split(".")
            for key in keys:
                result = result[key]
        return result

    def statusCode(code):
        assert (code == Validation.code) is True
        return Validation
    
    def expect(keys:str, string):
        keys = keys.split(".")
        result = Validation.response()
        for key in keys:
            result = result[key]
        result = str(result)
        assert (result == string) is True
        return Validation

class Rest:
    response: object = {}

    def post(url, body, headers={}, auth=("","")):
        res = requests.post(url=url, headers=headers,data=json.dumps(body), auth=auth)
        Rest.response = {"status_code":res.status_code, "response":res.json(), "headers":res.headers}
        Validation.code = res.status_code
        return Validation

    def get(url, headers={}, auth=("","")):
        res = requests.get(url=url, headers=headers, auth=auth)
        Rest.response = {"status_code":res.status_code, "response":res.json(), "headers":res.headers}
        Validation.code = res.status_code
        return Validation