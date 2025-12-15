import time

try:
    from gpiozero import DigitalInputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    DigitalInputDevice = None


class SoundSensor:
    """
    Gestion du capteur de son CrowPi (micro).

    Le capteur est binaire (0/1). On détecte un "bruit"
    sur le front montant (passage de 0 -> 1).
    """

    def __init__(self, pin=24, debounce_s=0.02):
        self.pin = pin
        self.debounce_s = debounce_s

        if DigitalInputDevice is not None:
            try:
                self.device = DigitalInputDevice(pin)
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
        Retourne (value, state) où :
        - value : 0 ou 1
        - state : "noise" sur front montant, sinon None.
        """
        value = self._read_raw()

        if self._last_value is None:
            self._last_value = value
            return value, None

        if value != self._last_value:
            # Petit anti-rebond
            time.sleep(self.debounce_s)
            value_confirm = self._read_raw()
            if value_confirm != value:
                return self._last_value, None

            previous = self._last_value
            self._last_value = value_confirm

            # On considère qu'un bruit est détecté sur front montant (0 -> 1)
            if previous == 0 and value_confirm == 1:
                return value_confirm, "noise"

        return self._last_value, None


sound_sensor = SoundSensor()

