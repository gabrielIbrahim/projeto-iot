import requests
import time
import random

# ================= CONFIG =================

URL = "https://projeto-iot-8fto.onrender.com/sensor"  # ALTERAR DEPOIS DO DEPLOY

# valores iniciais
temperature = 25.0
humidity = 60.0


# ================= LOOP =================

while True:

    try:
        # variação suave (simula ambiente real)
        temperature += random.uniform(-0.5, 0.5)
        humidity += random.uniform(-1.0, 1.0)

        # limites realistas
        temperature = max(10, min(40, temperature))
        humidity = max(20, min(90, humidity))

        data = {
            "temperature": round(temperature, 2),
            "humidity": round(humidity, 2)
        }

        response = requests.post(URL, json=data)

        print(f"Enviado: {data} | Status: {response.status_code}")

    except Exception as e:
        print("Erro ao enviar dados:", e)

    # intervalo seguro (IMPORTANTE)
    time.sleep(3)