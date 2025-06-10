from shared import canal_ultrason
import time

def detects_ultra():
    val = int((canal_ultrason.voltage / 3.3) * 1023)
    distance = val * 520 / 1023  # conversion à ajuster selon ton capteur
    return distance
