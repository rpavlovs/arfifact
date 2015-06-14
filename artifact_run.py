import pyaudio
import wave
import sys
import signal, os
import threading
from threading import Thread

import RPi.GPIO as GPIO
import time

# def ctrl_c_handler(signum, frame):
# 	GPIO.cleanup
#     print 'Signal handler called with signal', signum

# signal.signal(signal.CTRL_C_EVENT, ctrl_c_handler)

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10


class AudioRecorderSender(threading.Thread):

	def __init__(self):
		super(WorkerThread, self).__init__()

		self.stoprequest = threading.Event()

		self.p = pyaudio.PyAudio()
		self.stream = self.p.open(format=FORMAT,
			channels=CHANNELS,
			rate=RATE,
			input=True,
			output=True,
			frames_per_buffer=chunk,
			input_device_index = 1)

	def __del__(self):
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()

	def new_record(self, filename):
		self.filename = filename
		self.run()

	def stop(self):
		self.stoprequest.set()

	def run(self):

		wf = wave.open(filename, 'w')
		wf.setnchannels(1) # mono
		wf.setsampwidth(2) # paInt16 is 2 bytes?
		wf.setframerate(RATE)

		print "* recording"

		for i in range(0, RATE / chunk * RECORD_SECONDS):
			data = stream.read(chunk)
			wf.writeframes(data)
			if self.stoprequest.isSet():
				break

				print "* done"
				wf.close()

			# send the file to tony

posPin		= 16 # pin 36
negPin		= 20 # pin 38
helpPin 	= 21 # pin 40

led1Pin 	= 25 # pin 22
led2Pin 	= 8  # pin 24
led3Pin 	= 7  # pin 26


GPIO.cleanup
GPIO.setmode(GPIO.BCM)

GPIO.setup(posPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(negPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(helpPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(led1Pin, GPIO.OUT)
GPIO.setup(led2Pin, GPIO.OUT)
GPIO.setup(led3Pin, GPIO.OUT)

# GPIO.output(led1Pin, True)
# time.sleep(1)
# GPIO.output(led1Pin, False)
# GPIO.output(led2Pin, True)
# time.sleep(1)
# GPIO.output(led2Pin, False)
# GPIO.output(led3Pin, True)
# time.sleep(1)
# GPIO.output(led3Pin, False)

# while True:
# 	if (GPIO.input(posPin) == False): print("+")
# 	if (GPIO.input(negPin)) == False: print("-")
# 	if (GPIO.input(helpPin) == False): print("?")


isIdle = True

wasLowPos	= False
wasLowNeg	= False
wasLowHelp	= False

isHoldingPos	= False
isHoldingNeg	= False
isHoldingHelp	= False

lowLoopsPos  = 0
lowLoopsNeg	 = 0
lowLoopsHelp = 0

debounceCntPos  = 0
debounceCntNeg	= 0
debounceCntHelp = 0

isRecOn = False

thresh = 4000
debounce_tresh = 50

def blink_4_times(args):
	freq = 1
	for x in xrange(1,5):
		GPIO.output(args, True)
		time.sleep(0.5)
		GPIO.output(args, False)
		time.sleep(0.5)


def onPosHold():
	GPIO.output(led1Pin, True)
	print "Recording positive feedback"

def onNegHold():
	GPIO.output(led2Pin, True)
	print "Recording negative feedback"

def onHelpHold():
	print "Help?"


def onPosDown():
	Thread(target = blink_4_times, args = (led1Pin,)).start()
	print "Like"

def onNegDown():
	Thread(target = blink_4_times, args = (led2Pin,)).start()
	print "Dislike"

def onHelpDown():
	print "Help"


def onPosRelease():
	GPIO.output(led1Pin, False)
	print "Positive feedback sent"

def onNegRelease():
	GPIO.output(led2Pin, False)
	print "Negative feedback sent"

def onHelpRelease():
	GPIO.output(led1Pin, False)
	GPIO.output(led2Pin, False)
	print "... Help sent!"

print "Running..."

while True:

	isLowPos  = GPIO.input(posPin) == False
	isLowNeg  = GPIO.input(negPin) == False
	isLowHelp = GPIO.input(helpPin) == False

	if (isLowPos and wasLowPos):
		lowLoopsPos += 1
	elif (wasLowPos and lowLoopsPos > thresh):
		# release Hold
		isHoldingPos = False
		onPosRelease()
		lowLoopsPos = 0
		debounceCntPos = 0
	elif (wasLowPos):
		# Detect Press
		onPosDown()
		lowLoopsPos = 0
		debounceCntPos = 0

	if (isLowNeg and wasLowNeg):
		lowLoopsNeg += 1
	elif (wasLowNeg and lowLoopsNeg > thresh):
		isHoldingNeg = False
		onNegRelease()
		lowLoopsNeg = 0
		debounceCntNeg = 0
	elif (wasLowNeg):
		onNegDown()
		lowLoopsNeg = 0
		debounceCntNeg = 0

	if (isLowHelp and wasLowHelp):
		lowLoopsHelp += 1
	elif (wasLowHelp and lowLoopsHelp > thresh):
		isHoldingHelp = False
		onHelpRelease()
		lowLoopsHelp = 0
		debounceCntHelp = 0
	elif (wasLowHelp):
		onHelpDown()
		lowLoopsHelp = 0
		debounceCntHelp = 0

	# Debouncing
	if (isLowPos and not wasLowPos):
		debounceCntPos += 1
	if (isLowNeg and not wasLowNeg):
		debounceCntNeg += 1
	if (isLowHelp and not wasLowHelp):
		debounceCntHelp += 1

	if (debounceCntPos > debounce_tresh):
		wasLowPos  = isLowPos
	if (debounceCntNeg > debounce_tresh):
		wasLowNeg  = isLowNeg
	if (debounceCntHelp > debounce_tresh):
		wasLowHelp = isLowHelp

	# Detect Hold
	if (isHoldingPos == False and lowLoopsPos > thresh):
		isHoldingPos = True
		onPosHold()

	if (isHoldingNeg == False and lowLoopsNeg > thresh):
		isHoldingNeg = True
		onNegHold()

	if (isHoldingHelp == False and lowLoopsHelp > thresh):
		isHoldingHelp = True
		onHelpHold()

	# print("lowLoopsPos " + str(lowLoopsPos) + " isHoldingPos " + str(isHoldingPos)
	# 		+ " lowLoopsNeg " + str(lowLoopsNeg)
	# 		+ " lowLoopsHelp " + str(lowLoopsHelp))

# while True

	# check all the buttons
	# implement logic with


	# def start_recording(filename):

	# 	wf = wave.open(filename, 'w')
	# wf.setnchannels(1) # mono
	# wf.setsampwidth(2) # paInt16 is 2 bytes?
	# wf.setframerate(RATE)

	# print "* recording"
	# for i in range(0, RATE / chunk * RECORD_SECONDS):
	# 	data = stream.read(chunk)
	# 	wf.writeframes(data)

	# 	print "* done"
	# 	wf.close()

	# 	def stop_recording():

