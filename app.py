from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from database import init_db
from models import insert_data, get_recent_data, get_latest_status
from anomaly_model import get_anomalies
from ml_model import train_and_predict

app = Flask(__name__)
CORS(app)

init_db()


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/sensor", methods=["POST"])
def sensor():

    data = request.json

    temp = data.get("temperature")
    hum = data.get("humidity")

    if temp is None or hum is None:
        return jsonify({"error": "Dados inválidos"}), 400

    insert_data(temp, hum)

    return jsonify({"message": "Dados recebidos com sucesso"}), 201


@app.route("/data")
def data():

    df = get_recent_data()

    return df.to_json(orient="records")


@app.route("/status")
def status():

    return jsonify(get_latest_status())


@app.route("/predict")
def predict():

    return jsonify(train_and_predict())


@app.route("/anomalies")
def anomalies():

    return jsonify(get_anomalies())


if __name__ == "__main__":
    app.run(debug=True)