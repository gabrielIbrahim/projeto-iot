import requests
import random
import time

url = "http://127.0.0.1:5000/sensor"

while True:
    data = {
        "temperature": round(random.uniform(0, 50), 2),
        "humidity": round(random.uniform(20, 99), 2)
    }
    try:
        response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            print(f"✅ Sucesso: {response.json()['message']}")
        else:
            print(f"⚠️ Erro API {response.status_code}: {response.json()}")
    except Exception as e:
        print(f"⚠️ Erro API: {e}")
    time.sleep(2)