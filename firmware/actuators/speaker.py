import RPi.GPIO as GPIO
import time

SPEAKER_PIN = 27
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
pwm = GPIO.PWM(SPEAKER_PIN, 440)  # 440 Hz

def play_beep():
    print("Ding dong !")
    pwm.start(50)
    pwm.ChangeFrequency(523)
    time.sleep(0.2)
    pwm.ChangeFrequency(392)
    time.sleep(0.2)
    pwm.stop()
