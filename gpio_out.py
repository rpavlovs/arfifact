import RPi.GPIO as GPIO
import time

pin = 21

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

state = True

GPIO.output(pin, True)
time.sleep(30)
GPIO.output(pin, False)


# while True:
#	GPIO.output(7,True)
#	time.sleep(1)
#	GPIO.output(7,False)
#	time.sleep(1)
