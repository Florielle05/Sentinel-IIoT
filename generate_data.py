import sqlite3
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_industrial_data(n_points=200):
    # 1. Création du temps (1 point toutes les minutes)
    start_time = datetime.now() - timedelta(minutes=n_points)
    timestamps = [start_time + timedelta(minutes=i) for i in range(n_points)]
    
    # 2. Génération de la base normale (Moyenne 25°C, Écart-type 2)
    # C'est la loi normale : N(25, 2)
    data = np.random.normal(25, 2, n_points)
    
    # 3. Injection d'anomalies (5 points au hasard)
    anomaly_indices = np.random.choice(range(n_points), size=5, replace=False)
    for idx in anomaly_indices:
        data[idx] = np.random.uniform(80, 120) # Pics de chaleur critiques
        
    return timestamps, data

def save_to_db(timestamps, values):
    conn = sqlite3.connect("sentinel.db")
    cursor = conn.cursor()
    
    for t, v in zip(timestamps, values):
        statut = "nominal" if v < 80 else "anomaly"
        cursor.execute(
            "INSERT INTO Telemetry (valeur, statut, timestamp) VALUES (?, ?, ?)",
            (v, statut, t)
        )
    
    conn.commit()
    conn.close()
    print(f"✅ {len(values)} points générés dans sentinel.db")

if __name__ == "__main__":
    t, v = generate_industrial_data()
    save_to_db(t, v)
