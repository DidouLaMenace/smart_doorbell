import requests

# Récupérer la valeur dans le dotenv
import os
from dotenv import load_dotenv
load_dotenv()
PUSHBULLET_TOKEN = os.getenv("PUSHBULLET_TOKEN")

def send_notification(message):
    print(f"[NOTIFY] {message}")
    try:
        res = requests.post(
            "https://api.pushbullet.com/v2/pushes",
            headers={
                "Access-Token": PUSHBULLET_TOKEN,
                "Content-Type": "application/json"
            },
            json={
                "type": "note",
                "title": "Alerte sonnette",
                "body": message
            }
        )
        if res.status_code != 200:
            print(f"[ERROR] Pushbullet: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[ERROR] Notification: {e}")
