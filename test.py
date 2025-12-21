import pigpio
import time

PIN = 20
pi = pigpio.pi()

pi.set_mode(PIN, pigpio.INPUT)

last_tick = 0
pulses = []

def cbf(gpio, level, tick):
    global last_tick, pulses
    if last_tick:
        pulses.append(pigpio.tickDiff(last_tick, tick))
    last_tick = tick

cb = pi.callback(PIN, pigpio.EITHER_EDGE, cbf)

try:
    while True:
        time.sleep(0.1)
        if len(pulses) > 60:
            print("Pulses:", pulses)
            pulses.clear()
except KeyboardInterrupt:
    cb.cancel()
    pi.stop()
