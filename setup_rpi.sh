#!/bin/sh

sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev python-dev
git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
sudo python pyaudio/setup.py install

easy_install utils
