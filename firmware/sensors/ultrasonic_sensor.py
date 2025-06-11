from shared import canal_ultrason

def detects_ultra():
    voltage = canal_ultrason.voltage 
    VCC = 5.0  # ou 3.3 
    distance = (voltage / VCC) * 520
    return distance
