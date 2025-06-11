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

# def key_pressed():
#     dr, _, _ = select.select([sys.stdin], [], [], 0)
#     return dr != []

print("Système actif. En attente d'une détection ou d'un appui bouton...")

# fd = sys.stdin.fileno()
# old_settings = termios.tcgetattr(fd)
# tty.setcbreak(fd)

last_activity_time = 0
already_alerted = False

try:
    while True:
        # if key_pressed():
        #     if sys.stdin.read(1) == "\n":
        #         print("Demande d'arrêt du programme.")
        #         break

        current_time = time.time()
        activity_detected = False
        event_type = None

        try:
            if button.is_pressed():
                activity_detected = True
                event_type = "button"

            distance = ultrasonic_sensor.detects_ultra()
            if distance < 25:
                activity_detected = True
                event_type = "move"

            if sound_sensor.detect_sound():
                activity_detected = True
                event_type = "sound"

            if activity_detected:
                last_activity_time = current_time

                if not already_alerted:
                    print(f"🔔 Événement détecté : {event_type}")
                    speaker.play_beep()
                    send_event(event_type)
                    already_alerted = True

            # Si plus aucune activité depuis X secondes, on réarme
            if already_alerted and (current_time - last_activity_time) > COOLDOWN_DURATION:
                print("✅ Aucune activité depuis 30 secondes. Réactivation de l'alerte.")
                already_alerted = False

        except Exception as e:
            print(f"[ERROR] Capteur : {e}")

        time.sleep(0.2)

finally:
    # termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    GPIO.cleanup()
