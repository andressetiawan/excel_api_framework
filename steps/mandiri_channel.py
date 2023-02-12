from behave import *
from utils.rest import Rest as rs
from utils.utils import Utils as ut
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@given("prepare request data for mandiri payment")
def step_impl(context):
    context.data = ut.getBankRequestBody(bank_channel="mandiri", amount=44000)
    context.url = "https://api.sandbox.midtrans.com/v2/charge"
    context.headers = {"Content-Type":"application/json" , "Accept": "application/json"}

@when("send mandiri payment request")
def step_impl(context):
    context.res = rs.post(url=context.url, body=context.data, headers=context.headers, auth=context.auth).statusCode(200).response()
    context.key = context.res["bill_key"]
    context.code = context.res["biller_code"]
    context.id = context.res["order_id"]

@when("do payment using mandiri")
def step_impl(context):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get(url="https://simulator.sandbox.midtrans.com/mandiri/bill/index")
    biller_code_input = wait.until(EC.presence_of_element_located((By.NAME, "biller_code")))
    biller_code_input.send_keys(context.code)

    biller_key_input = wait.until(EC.presence_of_element_located((By.NAME, "bill_key")))
    biller_key_input.send_keys(context.key)

    btn_inquery = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[2]/form/div[3]/div/button')))
    btn_inquery.click()

    btn_pay = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[2]/form/div[5]/div/button')))
    btn_pay.click()