from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os

from models import save_data, get_data
from ml_model import predict_temperature, predict_humidity
from anomaly_model import detect_anomaly, save_anomaly, get_anomalies

from models import init_db

init_db()

app = Flask(__name__)
CORS(app)

# ================= HOME =================
@app.route("/")
def home():
    return render_template("dashboard.html")


# ================= RECEBER DADOS =================
@app.route("/sensor", methods=["POST"])
def sensor():

    data = request.json

    temperature = data.get("temperature")
    humidity = data.get("humidity")

    if temperature is None or humidity is None:
        return jsonify({"error": "Dados inválidos"}), 400

    save_data(temperature, humidity)

    # detectar anomalia
    if detect_anomaly(temperature, humidity):
        save_anomaly(temperature, humidity)

    return jsonify({"message": "Dados recebidos com sucesso"}), 201


# ================= DADOS =================
@app.route("/data", methods=["GET"])
def data():
    return jsonify(get_data())


# ================= PREVISÃO =================
@app.route("/predict", methods=["GET"])
def predict():

    temp_pred = predict_temperature()
    hum_pred = predict_humidity()

    return jsonify({
        "temperature": temp_pred,
        "humidity": hum_pred
    })


# ================= ANOMALIAS =================
@app.route("/anomalies", methods=["GET"])
def anomalies():
    return jsonify(get_anomalies())


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)