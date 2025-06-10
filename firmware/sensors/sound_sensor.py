from shared import canal_micro

def detect_sound():
    val = canal_micro.voltage
    return val > 0.2  # seuil ajustable
