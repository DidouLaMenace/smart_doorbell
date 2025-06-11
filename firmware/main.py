import time
import requests
import RPi.GPIO as GPIO
import sys
import termios
import tty
import select

from sensors import sound_sensor, button, ultrasonic_sensor
from actuators import speaker

BACKEND_URL = "http://localhost:5000/event"
COOLDOWN_DURATION = 30  # secondes

def send_event(event_type):
    try:
        requests.post(BACKEND_URL, json={"event_type": event_type})
    except Exception as e:
        print(f"[ERROR] Échec d'envoi de l'événement '{event_type}': {e}")

def key_pressed():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return dr != []

print("Système actif. En attente d'une détection ou d'un appui bouton...")

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)

last_detection_time = 0  # Temps de la dernière détection
detection_active = True  # État de détection autorisée

try:
    while True:
        if key_pressed():
            if sys.stdin.read(1) == "\n":
                print("Demande d'arrêt du programme.")
                break

        current_time = time.time()

        # Si cooldown passé, on réarme la détection
        if not detection_active and current_time - last_detection_time >= COOLDOWN_DURATION:
            print("✅ Fenêtre de détection réactivée.")
            detection_active = True

        try:
            event_triggered = False

            if detection_active:
                if button.is_pressed():
                    print("🔘 Bouton pressé")
                    event_triggered = "button"

                distance = ultrasonic_sensor.detects_ultra()
                if distance < 25:
                    print(f"📏 Présence détectée (distance = {distance:.2f} cm)")
                    event_triggered = "move"

                if sound_sensor.detect_sound():
                    print("🔊 Bruit détecté")
                    event_triggered = "sound"

                if event_triggered:
                    speaker.play_beep()
                    send_event(event_triggered)
                    last_detection_time = current_time
                    detection_active = False  # Désactive les futures détections pendant le cooldown

        except Exception as e:
            print(f"[ERROR] Capteur : {e}")

        time.sleep(0.2)

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    GPIO.cleanup()
