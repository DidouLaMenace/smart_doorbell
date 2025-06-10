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

def send_event(event_type):
    try:
        requests.post(BACKEND_URL, json={"event_type": event_type})
    except Exception as e:
        print(f"[ERROR] Échec d'envoi de l'événement '{event_type}': {e}")

def key_pressed():
    dr, _, _ = select.select([sys.stdin], [], [], 0)
    return dr != []

print("Système actif. En attente d'une détection ou d'un appui bouton...")

# Met le terminal en mode raw pour capter les touches
fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
tty.setcbreak(fd)

try:
    while True:
        if key_pressed():
            if sys.stdin.read(1) == "\n":
                print("Demande d'arrêt du programme.")
                break

        try:
            if button.is_pressed():
                print("Bouton pressé")
                speaker.play_beep()
                send_event("button")
        except Exception as e:
            print(f"[ERROR] Bouton : {e}")

        try:
            distance = ultrasonic_sensor.detects_ultra()
            if distance < 25:
                print(f"Présence détectée (distance = {distance:.2f} cm)")
                speaker.play_beep()
                send_event("move")
        except Exception as e:
            print(f"[ERROR] Ultrason : {e}")

        try:
            if sound_sensor.detect_sound():
                print("Bruit détecté")
                speaker.play_beep()
                send_event("sound")
        except Exception as e:
            print(f"[ERROR] Son : {e}")

        time.sleep(0.2)

# except KeyboardInterrupt:
#     print("🛑 Arrêt manuel")
#     GPIO.cleanup()

finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    GPIO.cleanup()
