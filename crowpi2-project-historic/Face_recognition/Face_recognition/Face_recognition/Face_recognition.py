import os
import time


os.system("lxterminal --title=detection --geometry=70x30+0+0 -e 'bash -c \"python Face_recognition0.py; exec bash\"'")
time.sleep(0.5)
os.system("wmctrl -r detection -b add,above")
