from behave import *
from utils.rest import Rest as rs
from utils.utils import Utils as ut
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@given("prepare request data for danamon online payment")
def step_impl(context):
    context.data = ut.getBankRequestBody(bank_channel="danamon", amount=44000)
    context.url = "https://api.sandbox.midtrans.com/v2/charge"
    context.headers = {"Content-Type":"application/json" , "Accept": "application/json"}

@when("send danamon online payment request")
def step_impl(context):
    context.res = rs.post(url=context.url, body=context.data, headers=context.headers, auth=context.auth).statusCode(200).expect("transaction_status", "pending").response()
    context.id = context.res["order_id"]
    print(context.res)

@when("do payment using danamon online")
def step_impl(context):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get(context.res["redirect_url"])
    btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[2]/form/div[3]/div/button')))
    btn_pay.click()