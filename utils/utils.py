import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class Utils:
    def generateRandomId():
        return f"uuid-{str(time.time()).split('.')[0]}"
    
    def getBankRequestBody(bank_channel:str, amount:int, desc1:str="", desc2:str=""):
        data = {}

        if bank_channel == "permata" or bank_channel == "bni" or bank_channel == "bca":
            data = { 
                "payment_type": "bank_transfer",
                "bank_transfer": {
                "bank": bank_channel
            },
                "transaction_details": {
                    "order_id": Utils.generateRandomId(),
                    "gross_amount": amount
                }
            }

        elif bank_channel == "cimb":
            data = {
                "payment_type": "cimb_clicks",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                },
                "cimb_clicks": {
                "description": desc1
                }
            }

        elif bank_channel == "danamon":
            data = {
                "payment_type": "danamon_online",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                }
            }

        elif bank_channel == "mandiri":
            data = {
                "payment_type": "echannel",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                },
                "echannel" : {
                    "bill_info1" : desc1,
                    "bill_info2" : desc2
                }
            }
        
        return data

    def payVirtualAccount(url, bank_channel, va_number):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        wait = WebDriverWait(driver=driver, timeout=10)
        driver.get(url=url)
        textfield = wait.until(EC.presence_of_element_located((By.NAME, "va_number")))
        textfield.send_keys(va_number)

        if bank_channel == "permata":
            btn_inquery = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div[2]/div/button")))
            btn_inquery.click()

            btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/form/div[3]/div/button")))
            btn_pay.click()
        
        elif bank_channel == "bni":
            btn_inquery = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[2]/form/div[2]/div/button')))
            btn_inquery.click()

            btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[2]/form/div[4]/div/button')))
            btn_pay.click()

        elif bank_channel == "bca":
            btn_inquery = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrap"]/div[2]/form/div[2]/div/button')))
            btn_inquery.click()

            btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="wrap"]/div[2]/form/div[4]/div/button')))
            btn_pay.click()

        driver.quit()