# import RPi.GPIO as GPIO
from gpiozero import InputDevice, Buzzer
import time

buzzer_pin = 18
# define sound pin
pir_pin = 23

# set GPIO mode to GPIO.BOARD
# GPIO.setmode(GPIO.BCM)
# setup pin as INPUT
# GPIO.setup(pir_pin, GPIO.IN)
# GPIO.setup(buzzer_pin, GPIO.OUT)

pir_sensor = InputDevice(pir_pin)
buzzer_sensor = Buzzer(buzzer_pin)



try:
    while True:
        # check if sound detected or not
        # the sound pin always HIGH unless sound detected, it goes LOW
        if(pir_sensor.value): 
            # Make buzzer sound
            # GPIO.output(buzzer_pin, GPIO.HIGH)
            buzzer_sensor.on()

        else:
            # Stop buzzer sound
            # GPIO.output(buzzer_pin, GPIO.LOW)
            buzzer_sensor.off()

except KeyboardInterrupt:
    #GPIO.output(buzzer_pin, GPIO.LOW)
    # GPIO.cleanup()
    pir_sensor.close()
    buzzer_sensor.close()
