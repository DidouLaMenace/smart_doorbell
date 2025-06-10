import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialisation du bus I2C et ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

canal_ultrason = AnalogIn(ads, ADS.P0)
canal_micro = AnalogIn(ads, ADS.P1)
