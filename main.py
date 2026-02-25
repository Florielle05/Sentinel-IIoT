from fastapi import FastAPI
import sqlite3
import joblib
import pandas as pd
from datetime import datetime

app = FastAPI()

# On charge le cerveau de l'IA au démarrage
try:
    model = joblib.load("modele_sentinel.pkl")
    print("🧠 Cerveau chargé avec succès !")
except:
    model = None
    print("⚠️ Attention : Aucun modèle trouvé. Lance train_model.py d'abord.")

@app.get("/test_capteur")
def test(temperature: float):
    # 1. Utiliser l'IA pour prédire
    if model:
        # L'IA attend un tableau, on lui donne la valeur
        prediction = model.predict([[temperature]])
        # Isolation Forest renvoie -1 pour une anomalie et 1 pour du normal
        statut_ia = "anomaly" if prediction[0] == -1 else "nominal"
    else:
        statut_ia = "Modèle non chargé"

    # 2. Enregistrement SQL (comme avant)
    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Telemetry (valeur, statut, timestamp) VALUES (?, ?, ?)",
        (temperature, statut_ia, datetime.now())
    )
    conn.commit()
    conn.close()

    return {
        "valeur": temperature,
        "prediction_IA": statut_ia,
        "message": "Anomalie détectée !" if statut_ia == "anomaly" else "Tout est OK"
    }

@app.get("/historique")
def get_history():
    conn = sqlite3.connect("sentinel.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Telemetry ORDER BY timestamp DESC LIMIT 10")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
