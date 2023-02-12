from behave import *
from utils.rest import Rest as rs
from utils.utils import Utils as ut
import time

@given(u'prepare request data for "{bank}" virtual account')
def step_impl(context, bank):
    context.start_time = time.time()
    context.bank = bank
    context.data = ut.getBankRequestBody(bank_channel=bank, amount=40000)
    print(context.data)
    context.url = "https://api.sandbox.midtrans.com/v2/charge"
    context.headers = {"Content-Type":"application/json" , "Accept": "application/json"}

@given(u'set request authentication')
def step_impl(context):
    context.server_key = "SB-Mid-server-mSMo_JSHHcWrWrrzwxRpDsri"
    context.auth = (context.server_key,"")

@when(u'send bank transfer request')
def step_impl(context):
    context.res = rs.post(url=context.url, body=context.data, headers=context.headers, auth=context.auth).statusCode(200).response()

    if context.bank == "permata":
        context.va = context.res["permata_va_number"]
        context.id = context.res["order_id"]
    elif (context.bank == "bni") or (context.bank == "bca") or (context.bank == "bri"):
        context.va = context.res["va_numbers"][0]["va_number"]
        context.id = context.res["order_id"]

@when(u'do payment using "{bank}"')
def step_impl(context, bank):
    bank_channel_url = {
        "permata": "https://simulator.sandbox.midtrans.com/permata/va/index",
        "bni": "https://simulator.sandbox.midtrans.com/bni/va/index",
        "bca": "https://simulator.sandbox.midtrans.com/bca/va/index",
        "bri": "https://simulator.sandbox.midtrans.com/bri/va/index"
    }

    ut.payVirtualAccount(bank_channel=bank, url=bank_channel_url.get(bank), va_number=context.va)

@then(u'do payment check')
def step_impl(context):
    rs.get(url=f'https://api.sandbox.midtrans.com/v2/{context.id}/status',auth=context.auth,headers=context.headers).statusCode(200).expect("transaction_status","settlement").response()