# Sentinel-IIoT 🛡️

Système de maintenance prédictive pour l'industrie.

## Fonctionnalités
- **Ingestion** : API temps réel avec FastAPI.
- **Stockage** : Base de données locale SQLite.
- **IA** : Détection d'anomalies via l'algorithme Isolation Forest (Unsupervised Learning).
- **Simulation** : Capteur virtuel générant des séries temporelles.

## Installation
```bash
pip install fastapi uvicorn scikit-learn pandas requests
