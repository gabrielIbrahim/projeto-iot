import sqlite3

DB_NAME = "database.db"


# ================= CRIAR BANCO =================
def init_db():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # tabela principal
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # tabela de anomalias
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS anomalies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            description TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


# ================= SALVAR DADOS =================
def save_data(temperature, humidity):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_data (temperature, humidity)
        VALUES (?, ?)
    """, (temperature, humidity))

    conn.commit()
    conn.close()


# ================= BUSCAR DADOS =================
def get_data(limit=50):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, temperature, humidity, timestamp
        FROM sensor_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    # inverter (mais antigo → mais novo)
    rows.reverse()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "temperature": row[1],
            "humidity": row[2],
            "timestamp": row[3]
        })

    return result