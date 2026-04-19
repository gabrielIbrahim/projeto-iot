from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

import threading
import time
import random
import requests
import os

from models import init_db, insert_data, get_last_data
from ml_model import predict_next
from anomaly_model import detect_anomaly, save_anomaly, get_anomalies

app = Flask(__name__)
CORS(app)

# ================= INICIALIZA BANCO =================
init_db()

# ================= ROTA DASHBOARD =================
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


# ================= ROTA RECEBER DADOS =================
@app.route("/sensor", methods=["POST"])
def receive_data():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Dados inválidos"}), 400

    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if temperature is None or humidity is None:
        return jsonify({"error": "Dados incompletos"}), 400

    insert_data(temperature, humidity)

    # detectar anomalia
    if detect_anomaly(temperature, humidity):
        save_anomaly(temperature, humidity)

    return jsonify({"status": "ok"}), 201


# ================= ROTA DADOS =================
@app.route("/data")
def get_data():
    data = get_last_data(limit=20)
    return jsonify(data)


# ================= ROTA PREVISÃO =================
@app.route("/predict")
def predict():
    try:
        result = predict_next()

        if not result:
            return jsonify({"error": "Dados insuficientes"}), 400

        return jsonify(result)

    except Exception as e:
        print("Erro na previsão:", e)
        return jsonify({"error": "Erro na previsão"}), 500


# ================= ROTA ANOMALIAS =================
@app.route("/anomalies")
def anomalies():
    return jsonify(get_anomalies())


# ================= SIMULADOR INTERNO =================
def simulator_loop():

    # URL local (funciona dentro do próprio servidor)
    URL = "http://127.0.0.1:5000/sensor"

    temperature = 25.0
    humidity = 60.0

    while True:
        try:
            temperature += random.uniform(-0.5, 0.5)
            humidity += random.uniform(-1.0, 1.0)

            temperature = max(10, min(40, temperature))
            humidity = max(20, min(90, humidity))

            data = {
                "temperature": round(temperature, 2),
                "humidity": round(humidity, 2)
            }

            requests.post(URL, json=data, timeout=2)

            print("Simulador interno:", data)

        except Exception as e:
            print("Erro no simulador:", e)

        time.sleep(5)


# ================= START DO SERVIDOR =================
if __name__ == "__main__":

    # inicia simulador em background
    threading.Thread(target=simulator_loop, daemon=True).start()

    # porta dinâmica (Render)
    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)