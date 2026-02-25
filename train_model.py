import sqlite3
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

def train_sentinel():
    # 1. Connexion et lecture via Pandas
    conn = sqlite3.connect("sentinel.db")
    # On transforme la table SQL en DataFrame (tableau de données)
    df = pd.read_sql_query("SELECT valeur FROM Telemetry", conn)
    conn.close()

    print(f"Données chargées : {len(df)} points.")

    # 2. Configuration de l'Isolation Forest
    # n_estimators : nombre d'arbres dans la forêt
    # contamination : proportion estimée d'anomalies (on a mis 5/200 = 0.025)
    model = IsolationForest(n_estimators=100, contamination=0.03, random_state=42)

    # 3. Entraînement
    # L'IA regarde toutes les valeurs et apprend à "isoler" les plus bizarres
    model.fit(df[['valeur']])

    # 4. Sauvegarde du modèle
    # On enregistre le cerveau dans un fichier .pkl pour que l'API puisse l'utiliser
    joblib.dump(model, "modele_sentinel.pkl")
    print("✅ Modèle entraîné et sauvegardé sous 'modele_sentinel.pkl'")

if __name__ == "__main__":
    train_sentinel()
