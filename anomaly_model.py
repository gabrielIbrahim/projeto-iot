import sqlite3
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest

DB_NAME = "database.db"


def load_recent_data(limit=100):
    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        f"""
        SELECT temperature, humidity
        FROM sensor_data
        ORDER BY id DESC
        LIMIT {limit}
        """,
        conn
    )

    conn.close()

    if df.empty:
        return None

    return df.iloc[::-1]  # inverter ordem


def detect_anomaly(temp, hum):

    df = load_recent_data()

    if df is None or len(df) < 10:
        return False

    X = df[["temperature", "humidity"]].values

    model = IsolationForest(
        contamination=0.05,
        random_state=42
    )

    model.fit(X)

    new_point = np.array([[temp, hum]])

    prediction = model.predict(new_point)

    return prediction[0] == -1  # -1 = anomalia


def save_anomaly(temp, hum, description="Anomalia detectada"):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO anomalies (temperature, humidity, description)
        VALUES (?, ?, ?)
    """, (temp, hum, description))

    conn.commit()
    conn.close()


def get_anomalies():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        "SELECT * FROM anomalies ORDER BY id DESC LIMIT 50",
        conn
    )

    conn.close()

    return df.to_dict(orient="records")