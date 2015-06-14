import pyaudio
import wave
import sys


chunk = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 10


if len(sys.argv) < 2:
    print("Records a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
	dev = p.get_device_info_by_index(i)
	print((i,dev['name'],dev['maxInputChannels']))

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                frames_per_buffer=chunk)

wf = wave.open(sys.argv[1], 'w')
wf.setnchannels(1) # mono
wf.setsampwidth(2) # paInt16 is 2 bytes?
wf.setframerate(RATE)


print "* recording"
for i in range(0, RATE / chunk * RECORD_SECONDS):
    data = stream.read(chunk)
    wf.writeframes(data)

print "* done"


wf.close()

stream.stop_stream()
stream.close()

p.terminate()
