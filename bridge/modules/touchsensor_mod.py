import time

try:
    from gpiozero import InputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    InputDevice = None


class TouchSensor:
    """
    Gestion du capteur tactile CrowPi en mode événementiel.

    API similaire à ButtonMatrix.step():
    - front montant (0 -> 1)  -> retourne (value, "down")
    - front descendant (1 -> 0) -> retourne (value, "up")
    - sinon                     -> retourne (value, None)
    """

    def __init__(self, pin=17, debounce_s=0.05):
        self.pin = pin
        self.debounce_s = debounce_s

        if InputDevice is not None:
            try:
                self.device = InputDevice(pin)
            except Exception:
                # En cas d'erreur d'initialisation GPIO, on désactive proprement
                self.device = None
        else:
            self.device = None

        self._last_value = None

    def _read_raw(self):
        if self.device is None:
            # Sur une machine sans GPIO, on renvoie 0
            return 0
        try:
            return int(self.device.value)
        except Exception:
            # En cas d'erreur ponctuelle, on garde l'ancienne valeur
            return 0 if self._last_value is None else self._last_value

    def step(self):
        """
        Lecture + détection de fronts.

        Retourne (value, state) où :
        - value : 0 ou 1
        - state : "down", "up" ou None
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
                # Variation due au bruit, on ignore
                return self._last_value, None

            previous = self._last_value
            self._last_value = value_confirm

            if previous == 0 and value_confirm == 1:
                return value_confirm, "down"
            if previous == 1 and value_confirm == 0:
                return value_confirm, "up"

        return self._last_value, None


touch_sensor = TouchSensor()

