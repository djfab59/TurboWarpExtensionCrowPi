#!/usr/bin/env python3
import time
from gpiozero import InputDevice

PIN = 20  # GPIO du récepteur IR sur le CrowPi (à adapter si besoin)

ir = InputDevice(PIN)

print("IR debug sur GPIO", PIN)
print("Appuie sur des boutons de la télécommande (Ctrl+C pour quitter)\n")

last_state = ir.value
last_time = time.time()

try:
    while True:
        v = ir.value
        if v != last_state:
            now = time.time()
            dt_ms = (now - last_time) * 1000.0
            level = "LOW " if v == 0 else "HIGH"
            print(f"{now:.6f}  {level}  (Δ ≈ {dt_ms:6.2f} ms)")
            last_state = v
            last_time = now

        # petit sleep pour ne pas saturer le CPU
        time.sleep(0.0005)
except KeyboardInterrupt:
    print("\nArrêt demandé, bye.")
