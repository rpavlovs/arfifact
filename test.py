import RPi.GPIO as GPIO


import time
import os

notBusy=1
countdown=5  
doingNothing=1
posPress=0
negPress=0
helpPress=0

startPosRecord
startNegRecord
startHelpRecord


isPosDown()
isNegDown()
isHelpDown()
startPosRecording
stopPosRecording
startNegRecording
stopNegRecording
startHelp
stopHelp



while true:
  if (doingNothing):
    if(posButtonPress):
      doingNothing=0
      posPress=1
    if(negButtonPress):
      doingNothing=0
      negPress=1
    if(helpPress):
      doingNothing=0
      helpPress=1
  

  #reset countdown or increase timer.
  if(notBusy):
    if(posPress && !isPosDown):
      doingNothing=1
      posPress=0

    if(negPress && !isNegDown):
      doingNothing=1
      negPress=0

    if(posPress && !ishelpDown):
      doingNothing=1
      helpPress=0

    if(posPress && isPosDown):
      countdown-=1

    if(negPress && isNegDown):
      countdown-=1

    if(posPress && ishelpDown):
      countdown-=1


  #stop recording
  if(startPosRecording && !isPosDown):
    notBusy=1;
    doingNothing=1;
    stopPosRecording()
  
  #stop recording
  if(startNegRecording && !isNegDown):
    notBusy=1;
    doingNothing=1;
    stopNegRecording()
    
  #stop help
    if(startHelp && !ishelpDown):
      stopHelp();


  #start action if press is down for more than .5 seconds.
  if(countdown<=0):
    countdown=5;
    notBusy=1
    
    if(posPress):
      startPosRecord=1
      startPosRecording()
      
    if(negPress):
      startNegRecord=1
      startNegRecording()
      
    if(helpPress):
      startHelp=1
  
  
  
    







