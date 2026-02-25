import requests
import time
import random

# L'adresse de notre API
URL = "http://127.0.0.1:8000/test_capteur"

print("📡 Démarrage du capteur IIoT (Ctrl+C pour arrêter)...")

while True:
    # On simule une température normale la plupart du temps
    # Mais on ajoute une chance de 10% d'avoir un pic anormal
    if random.random() < 0.1:
        temp = random.uniform(80, 120)  # Anomalie
    else:
        temp = random.uniform(22, 28)   # Normal
    
    try:
        # On envoie la donnée à l'API via le réseau
        response = requests.get(URL, params={"temperature": temp})
        data = response.json()
        
        print(f"🌡️ Temp: {temp:.2f}°C | IA: {data['prediction_IA']} | {data['message']}")
    except Exception as e:
        print(f"❌ Erreur de connexion : {e}")
    
    time.sleep(2) # On attend 2 secondes avant la prochaine mesure
