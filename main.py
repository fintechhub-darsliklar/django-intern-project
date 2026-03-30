
import requests


url = "http://127.0.0.1:8000/api/v1/rpc-client/"

test = {"jsonrpc": "2.0", "result": "pong", "id": 1}

data = {
    "id": 1,
    "method": "transfer_create",
    "params": {
        "id": 9
    }
}


result = requests.post(url, json=test)

print(result.json())





# 5 sekund

# 6000




