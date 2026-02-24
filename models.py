import sqlite3
import pandas as pd

from anomaly_model import detect_anomaly, save_anomaly

DB_NAME = "database.db"


def insert_data(temp, hum):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data (temperature, humidity)
        VALUES (?, ?)
    """, (temp, hum))

    conn.commit()
    conn.close()

    # verificar anomalia
    if detect_anomaly(temp, hum):
        save_anomaly(temp, hum)


def get_recent_data(limit=20):

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        f"""
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
        LIMIT {limit}
        """,
        conn
    )

    conn.close()

    return df.iloc[::-1]


def get_latest_status():

    conn = sqlite3.connect(DB_NAME)

    df = pd.read_sql_query(
        """
        SELECT *
        FROM sensor_data
        ORDER BY id DESC
        LIMIT 1
        """,
        conn
    )

    conn.close()

    if df.empty:
        return {}

    return df.iloc[0].to_dict()