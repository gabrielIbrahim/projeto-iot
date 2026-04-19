from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import threading
import time
import random
import requests
import os

from models import init_db, save_data, get_data
from ml_model import predict_temperature, predict_humidity
from anomaly_model import detect_anomaly, save_anomaly, get_anomalies

app = Flask(__name__)
CORS(app)

# ================= INIT DB =================
init_db()

# ================= ROTAS =================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/sensor", methods=["POST"])
def receive_data():
    data = request.get_json()

    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if temperature is None or humidity is None:
        return jsonify({"error": "dados inválidos"}), 400

    save_data(temperature, humidity)

    if detect_anomaly(temperature, humidity):
        save_anomaly(temperature, humidity)

    return jsonify({"status": "ok"}), 201


@app.route("/data")
def data():
    return jsonify(get_data())


@app.route("/predict")
def predict():
    try:
        return jsonify({
            "temperature": predict_temperature(),
            "humidity": predict_humidity()
        })
    except Exception as e:
        print("Erro ML:", e)
        return jsonify({"error": "erro ML"}), 500


@app.route("/anomalies")
def anomalies():
    return jsonify(get_anomalies())


# ================= SIMULADOR MELHORADO =================
def simulator_loop():

    port = os.environ.get("PORT", "5000")
    url = f"http://127.0.0.1:{port}/sensor"

    print("Simulador iniciado em:", url)

    # espera o servidor subir
    time.sleep(5)

    temp = 25.0
    hum = 60.0

    trend = 0.2  # tendência inicial

    while True:
        try:
            # 🔥 tendência dinâmica
            if random.random() < 0.1:
                trend *= -1  # inverte direção

            temp += trend + random.uniform(-0.3, 0.3)

            # 🔥 umidade inversamente correlacionada
            hum += (-trend * 2) + random.uniform(-1.5, 1.5)

            # 🔥 limites realistas
            temp = max(10, min(40, temp))
            hum = max(20, min(90, hum))

            # 🔥 INJEÇÃO DE ANOMALIA (visual forte)
            if random.random() < 0.08:
                print("⚠️ GERANDO ANOMALIA!")

                temp += random.choice([-8, 8])
                hum += random.choice([-20, 20])

            data = {
                "temperature": round(temp, 2),
                "humidity": round(hum, 2)
            }

            response = requests.post(url, json=data, timeout=3)

            print("OK:", data, "|", response.status_code)

        except Exception as e:
            print("Erro simulador:", e)

        time.sleep(5)


# ================= START =================
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    # inicia simulador em background
    threading.Thread(target=simulator_loop, daemon=True).start()

    print("Servidor rodando na porta:", port)

    app.run(host="0.0.0.0", port=port)