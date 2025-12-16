#!/bin/bash

# Lancer le script Python en arrière-plan
python3 /home/pi/TurboWarpExtensionCrowPi/run.py &
RUN_PID=$!

# Lancer TurboWarp (au premier plan)
turbowarp-desktop

# Quand TurboWarp se ferme, tuer run.py
kill $RUN_PID

