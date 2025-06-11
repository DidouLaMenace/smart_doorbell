import RPi.GPIO as GPIO
import time

SPEAKER_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
pwm = GPIO.PWM(SPEAKER_PIN, 440)  # 440 Hz

# Notes (fréquences en Hz)
notes = {
    'C5': 523,
    'D5': 587,
    'E5': 659,
    'F5': 698,
    'G5': 784,
    'A5': 880,
    'B5': 988,
    'C6': 1047
}


def play_beep():
    print("Ding dong !")
    pwm.start(50)

    melody = [
        ('C5', 0.2),
        ('E5', 0.2),
        ('G5', 0.2),
        ('C6', 0.3),
        (None, 0.1),
    ]

    for note, duration in melody:
        if note:
            pwm.ChangeFrequency(notes[note])
        else:
            pwm.ChangeFrequency(1)  # quasi silence
        time.sleep(duration)

    pwm.stop()
