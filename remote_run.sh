#/bin/sh

scp ./artifact_run.py rpi:~/artifact
ssh rpi "sudo python ~/artifact/artifact_run.py"

