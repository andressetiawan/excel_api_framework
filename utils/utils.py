import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from utils.bank_channel import bank_channel as BC

class Utils:

    def generateRandomId():
        return f"uuid-{str(time.time()).split('.')[0]}"
    
    def getBankRequestBody(bank_channel:str, amount:int):
        data = {}

        if (bank_channel == BC.PERMATA) or (bank_channel == BC.BNI) or (bank_channel == BC.BCA) or (bank_channel == BC.BRI):
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

        elif bank_channel == BC.CIMB:
            data = {
                "payment_type": "cimb_clicks",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                },
                "cimb_clicks": {
                "description": "Purchase description"
                }
            }

        elif bank_channel == BC.DANAMON:
            data = {
                "payment_type": "danamon_online",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                }
            }

        elif bank_channel == BC.MANDIRI:
            data = {
                "payment_type": "echannel",
                "transaction_details": {
                    "gross_amount": amount,
                    "order_id": Utils.generateRandomId()
                },
                "echannel" : {
                    "bill_info1" : "Billing information 1",
                    "bill_info2" : "Billing information 2"
                }
            }
        
        return data

    def payVirtualAccount(url, bank_channel:str, va_number):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        wait = WebDriverWait(driver=driver, timeout=10)
        driver.get(url=url)
        textfield = wait.until(EC.presence_of_element_located((By.NAME, "va_number")))
        textfield.send_keys(va_number)

        btn_inquery_xpaths = {
            "permata" : '/html/body/div[2]/form/div[2]/div/button',
            "bni": '//*[@id="wrap"]/div[2]/form/div[2]/div/button',
            "bca": '//*[@id="wrap"]/div[2]/form/div[2]/div/button',
            "bri": '//*[@id="wrap"]/div[2]/form/div[2]/div/button'
        }

        btn_pay_xpaths = {
            "permata" : '/html/body/div[2]/form/div[3]/div/button',
            "bni": '//*[@id="wrap"]/div[2]/form/div[4]/div/button',
            "bca": '//*[@id="wrap"]/div[2]/form/div[4]/div/button',
            "bri": '//*[@id="wrap"]/div[2]/form/div[3]/div/button'
        }

        btn_inquery = wait.until(EC.presence_of_element_located((By.XPATH, btn_inquery_xpaths.get(bank_channel))))
        btn_inquery.click()

        btn_pay = wait.until(EC.presence_of_element_located((By.XPATH, btn_pay_xpaths.get(bank_channel))))
        btn_pay.click()

        driver.quit()