from behave import *
from utils.rest import Rest as rs
from utils.utils import Utils as ut
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

@given(u'prepare request data')
def step_impl(context):
    context.start_time = time.time()
    context.id = ut.generateRandomId()
    context.data = {
        "payment_type": "bank_transfer",
        "bank_transfer": {
            "bank": "permata"
        },
        "transaction_details": {
            "order_id": context.id,
            "gross_amount": 44000
        }
    }
    context.url = "https://api.sandbox.midtrans.com/v2/charge"
    context.headers = {"Content-Type":"application/json" , "Accept": "application/json"}

@given(u'set request authentication')
def step_impl(context):
    context.server_key = "SB-Mid-server-mSMo_JSHHcWrWrrzwxRpDsri"
    context.auth = (context.server_key,"")

@when(u'send the request')
def step_impl(context):
    context.res = rs.post(url=context.url, body=context.data, headers=context.headers, auth=context.auth).statusCode(200).expect("status_message", "Success, PERMATA VA transaction is successful").response()
    context.va = context.res["response"]["permata_va_number"]

@when(u'do payment')
def step_impl(context):
    context.driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(context.driver, 10)
    context.driver.get("https://simulator.sandbox.midtrans.com/permata/va/index")
    textfield = wait.until(EC.presence_of_element_located((By.NAME, "va_number")))
    textfield.send_keys(context.va)

    btn_inquery = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div[2]/div/button")))
    btn_inquery.click()

    btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div[3]/div/button")))
    btn_pay.click()

@then(u'do payment check')
def step_impl(context):
    res = rs.get(url=f'https://api.sandbox.midtrans.com/v2/{context.id}/status',auth=context.auth,headers=context.headers).statusCode(200).expect("transaction_status","settlement").response()