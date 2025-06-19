from shared import canal_micro

import time

duration = 0.2  # Durée d'écoute en secondes
sample_rate = 100  # Fréquence d'échantillonnage en Hz

def detect_sound():
    samples = []
    start_time = time.time()
    while time.time() - start_time < duration:
        val = canal_micro.voltage
        samples.append(val)
        time.sleep(1 / sample_rate)

    baseline = min(samples)  # ou moyenne basse pour bruit de fond
    peak = max(samples)
    variation = peak - baseline
    return variation > 0.016
