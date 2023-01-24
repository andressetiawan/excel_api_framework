from utils.utils import *
from utils.rest import Rest as rs

server_key = "SB-Mid-server-mSMo_JSHHcWrWrrzwxRpDsri"
auth = (server_key,"")
headers = {"Content-Type":"application/json" , "Accept": "application/json"}
url = "https://api.sandbox.midtrans.com/v2/charge"
data = {
    "payment_type": "bank_transfer",
    "bank_transfer": {
        "bank": "permata"
    },
    "transaction_details": {
        "order_id": Utils.generateRandomId(),
        "gross_amount": -44000
    }
}

res = rs.post(url=url, body=data, headers=headers, auth=auth).expect("validation_messages", "['transaction_details.gross_amount must be greater than or equal to 1']")