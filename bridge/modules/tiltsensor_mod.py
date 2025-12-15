import time

try:
    from gpiozero import InputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    InputDevice = None


class TiltSensor:
    """
    Gestion du capteur d'inclinaison (tilt) CrowPi.

    Le capteur est binaire (0/1). On le mappe directement sur deux états :
    - 1 -> "left"
    - 0 -> "right"
    """

    def __init__(self, pin=22, debounce_s=0.05):
        self.pin = pin
        self.debounce_s = debounce_s

        if InputDevice is not None:
            try:
                self.device = InputDevice(pin)
            except Exception:
                self.device = None
        else:
            self.device = None

        self._last_value = None

    def _read_raw(self):
        if self.device is None:
            return 0
        try:
            return int(self.device.value)
        except Exception:
            return 0 if self._last_value is None else self._last_value

    def step(self):
        """
        Retourne (value, direction) où :
        - value      : 0 ou 1
        - direction  : "left", "right" ou None (si pas de changement)
        """
        value = self._read_raw()

        if self._last_value is None:
            self._last_value = value
            return value, None

        if value != self._last_value:
            time.sleep(self.debounce_s)
            value_confirm = self._read_raw()
            if value_confirm != value:
                return self._last_value, None

            self._last_value = value_confirm
            direction = "left" if value_confirm == 1 else "right"
            return value_confirm, direction

        return self._last_value, None


tilt_sensor = TiltSensor()

