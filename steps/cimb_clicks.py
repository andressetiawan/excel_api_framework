from behave import *
from utils.rest import Rest as rs
from utils.utils import Utils as ut
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

@given("prepare request data for CIMB Clicks")
def step_impl(context):
    context.data = ut.getBankRequestBody(bank_channel="cimb", amount=44000)
    context.url = "https://api.sandbox.midtrans.com/v2/charge"
    context.headers = {"Content-Type":"application/json" , "Accept": "application/json"}

@when("send CIMB Clicks request")
def step_impl(context):
    context.res = rs.post(url=context.url, body=context.data, headers=context.headers, auth=context.auth).statusCode(200).expect("transaction_status", "pending").response()
    context.id = context.res["order_id"]

@when("do payment using CIMB Clicks")
def step_impl(context):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    wait = WebDriverWait(driver=driver, timeout=10)
    driver.get(context.res["redirect_url"])
    accountInput = wait.until(EC.presence_of_element_located((By.NAME, "AccountId")))
    accountInput.send_keys("testuser00")
    btn_pay = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrap"]/div[2]/form[1]/div[2]/div/button')))
    btn_pay.click()