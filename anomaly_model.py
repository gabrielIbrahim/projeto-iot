import sqlite3
import pandas as pd
import numpy as np

from sklearn.ensemble import IsolationForest

DB_NAME = "database.db"


# ================= CARREGAR DADOS =================
def load_recent_data(limit=100):

    try:
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

        # inverter ordem (antigo -> novo)
        return df.iloc[::-1]

    except Exception as e:
        print("Erro ao carregar dados:", e)
        return None


# ================= DETECTAR ANOMALIA =================
def detect_anomaly(temp, hum):

    try:
        df = load_recent_data()

        # poucos dados → não detecta
        if df is None or len(df) < 10:
            return False

        X = df[["temperature", "humidity"]].values

        model = IsolationForest(
            contamination=0.05,
            random_state=42,
            n_estimators=50  # leve para produção
        )

        model.fit(X)

        new_point = np.array([[temp, hum]])

        prediction = model.predict(new_point)

        return prediction[0] == -1  # -1 = anomalia

    except Exception as e:
        print("Erro na detecção de anomalia:", e)
        return False


# ================= SALVAR ANOMALIA =================
def save_anomaly(temp, hum, description="Anomalia detectada"):

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO anomalies (temperature, humidity, description)
            VALUES (?, ?, ?)
        """, (temp, hum, description))

        conn.commit()
        conn.close()

    except Exception as e:
        print("Erro ao salvar anomalia:", e)


# ================= BUSCAR ANOMALIAS =================
def get_anomalies(limit=50):

    try:
        conn = sqlite3.connect(DB_NAME)

        df = pd.read_sql_query(
            f"SELECT * FROM anomalies ORDER BY id DESC LIMIT {limit}",
            conn
        )

        conn.close()

        return df.to_dict(orient="records")

    except Exception as e:
        print("Erro ao buscar anomalias:", e)
        return []