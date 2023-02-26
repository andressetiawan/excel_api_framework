from behave import *
import pandas as pd
import time
import requests
import ast
from jsonschema import validate
from jsonschema.exceptions import ValidationError
import uuid

df = pd.read_excel("/home/andres/Documents/skripsi/python-bdd/input/Test Scenario Payment Gateway Midtrans copy.xlsx", index_col=0)

@given("Prepare testing request data and headers")
def prepare_testing_request_data_and_headers(context):
    context.api_urls = df["API URL"].values.tolist()
    context.methods = df["Method"].values.tolist()
    context.scenarios = df["Scenario"].values.tolist()
    context.exptResult = df["Expected result"].values.tolist()
    context.body = df["Request body"].values.tolist()
    context.headers = df["Headers"].values.tolist()
    context.qData = df["Query data"].values.tolist()

    context.data_prep = {}
    for i in range(0, df.shape[0]):
        context.data_prep[context.scenarios[i]] = {
            "api_url" : context.api_urls[i],
            "method":context.methods[i],
            "reqBody": context.body[i],
            "exptResult": context.exptResult[i],
            "headers":context.headers[i],
            "query": context.qData[i]
        }

    for scenario in context.scenarios:
        api_url = context.data_prep.get(scenario)["api_url"]

        req_body = {} if not type(context.data_prep.get(scenario)["reqBody"]) == str else context.data_prep.get(scenario)["reqBody"]

        if("{{$uuid}}" in req_body):
            req_body = req_body.replace("{{$uuid}}", str(uuid.uuid4()))

        context.data_prep.get(scenario)["reqBody"] = req_body

        params = []
        if "{{" in api_url or "}}" in api_url:
            urlList = api_url.split("{{")
            for url in urlList:
                if "}}" in url:
                    params.append(url.split("}}")[0])
        

        for param in params:
            api_url = api_url.replace('{{' + param + '}}' , str(ast.literal_eval(context.data_prep.get(scenario)["query"]).get(param)))

        context.data_prep.get(scenario)["api_url"] = api_url

@when("Client send request data")
def client_send_request_data(context):
    start_time = time.time()
    context.result = []

    for scenario in context.scenarios:
        currentRequest = context.data_prep.get(scenario)
        headers_req = {} if not type(currentRequest['headers']) == str else ast.literal_eval(currentRequest["headers"])
        res = {}

        if(currentRequest["method"] == "POST"):
            res = requests.post(url=currentRequest["api_url"], headers=headers_req, data=currentRequest["reqBody"]).json()
        elif(currentRequest["method"] == "GET"):
            res = requests.get(url=currentRequest["api_url"], headers=headers_req).json()
        
        end_time = time.time()
        ext_time = end_time - start_time
        context.result.append({
            "response" : res,
            "execution_time": ext_time
        })

        start_time = time.time()
            
@then("System checks json schema")
def system_checks_json_schema(context):
    context.status = []
    for i in range(0, len(context.result)):
        res = context.result[i].get("response")
        schema = ast.literal_eval(context.exptResult[i])
        print("=" * 60 + "RESPONSE" + "=" * 60)
        print(res)
        try:
            context.status.append(validate(instance=res, schema=schema) == None)
        except ValidationError as ex:
            context.status.append(False)

    context.api_urls = df["API URL"].values.tolist()
    context.methods = df["Method"].values.tolist()
    context.scenarios = df["Scenario"].values.tolist()
    context.exptResult = df["Expected result"].values.tolist()
    context.headers = df["Headers"].values.tolist()

@then("System generate report")
def system_generate_report(context):
    actual_result = []
    ext_times = []
    for d in context.result:
        actual_result.append(d.get("response"))
        ext_times.append(d.get("execution_time"))

    df["Status"] = context.status
    df["Response time"] = ext_times
    df["Actual result"] = actual_result

    df.to_excel(f"./output/{str(time.time()).split('.')[0]}_testReport.xlsx",index=True)