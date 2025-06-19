import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
pin = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
try:
    
    while True:
        GPIO.output(pin, 0)
        print("relay on")
        time.sleep(1)
        GPIO.output(pin, 1)
        print("relay off")
        time.sleep(1)
finally:
    GPIO.cleanup()
