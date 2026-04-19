import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

DB_NAME = "database.db"


# ================= CARREGAR DADOS =================
def load_data(limit=50):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT temperature, humidity
        FROM sensor_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 5:
        return None

    rows.reverse()

    temps = [r[0] for r in rows]
    hums = [r[1] for r in rows]

    return temps, hums


# ================= PREVISÃO TEMPERATURA =================
def predict_temperature():

    data = load_data()

    if data is None:
        return {"predictions": [0]}

    temps, _ = data

    try:
        X = np.arange(len(temps)).reshape(-1, 1)
        y = np.array(temps)

        model = LinearRegression()
        model.fit(X, y)

        next_x = np.array([[len(temps)]])
        prediction = model.predict(next_x)[0]

        return {"predictions": [float(prediction)]}

    except Exception as e:
        print("Erro ML temperatura:", e)
        return {"predictions": [temps[-1]]}


# ================= PREVISÃO UMIDADE =================
def predict_humidity():

    data = load_data()

    if data is None:
        return {"predictions": [0]}

    _, hums = data

    try:
        X = np.arange(len(hums)).reshape(-1, 1)
        y = np.array(hums)

        model = LinearRegression()
        model.fit(X, y)

        next_x = np.array([[len(hums)]])
        prediction = model.predict(next_x)[0]

        return {"predictions": [float(prediction)]}

    except Exception as e:
        print("Erro ML umidade:", e)
        return {"predictions": [hums[-1]]}