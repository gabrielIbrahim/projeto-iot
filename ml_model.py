import sqlite3
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error


DB_NAME = "database.db"


# =========================
# Carregar dados do banco
# =========================
def load_data():
    conn = sqlite3.connect(DB_NAME)

    try:
        df = pd.read_sql_query(
            "SELECT temperature, humidity FROM sensor_data ORDER BY id",
            conn
        )
    except Exception:
        df = pd.DataFrame()

    conn.close()
    return df


# =========================
# Criar janelas temporais
# =========================
def create_windows(series, window_size=3):
    X = []
    y = []

    for i in range(len(series) - window_size):
        X.append(series[i:i + window_size])
        y.append(series[i + window_size])

    return np.array(X), np.array(y)


# =========================
# Treinar modelo e prever
# =========================
def train_and_predict(steps=5):

    df = load_data()

    if df.empty or len(df) < 10:
        return {
            "error": "Dados insuficientes para previsão"
        }

    results = {}

    for column in ["temperature", "humidity"]:

        data = df[column].values

        X, y = create_windows(data, window_size=3)

        if len(X) < 5:
            return {"error": "Poucas amostras"}

        model = LinearRegression()
        model.fit(X, y)

        # ===== erro do modelo =====
        y_pred = model.predict(X)
        rmse = float(np.sqrt(mean_squared_error(y, y_pred)))

        # ===== previsão multi-passo =====
        last_window = data[-3:].copy()
        predictions = []

        for _ in range(steps):
            next_value = model.predict([last_window])[0]
            predictions.append(float(next_value))

            last_window = np.roll(last_window, -1)
            last_window[-1] = next_value

        results[column] = {
            "current": float(data[-1]),
            "predictions": predictions,
            "confidence_interval": [
                float(predictions[0] - rmse),
                float(predictions[0] + rmse)
            ],
            "rmse": rmse
        }

    return {
        "temperature": results["temperature"],
        "humidity": results["humidity"],
        "steps_ahead": steps,
        "samples_used": int(len(df))
    }