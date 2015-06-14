import RPi.GPIO as GPIO
import time
import os

pin = 7

GPIO.cleanup

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

cnt = 1

while True:
	
	# print( "GPIO.input: " + str( GPIO.input(pin) ) );
	
	if (GPIO.input(pin) == False):
		print("Button Pressed " + str(cnt))
		cnt += 1
		# time.sleep( 0.2 )

	
