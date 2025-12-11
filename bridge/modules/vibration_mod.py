import time
from typing import Optional

from gpiozero import OutputDevice


class Vibration:
    """
    Contrôle d'un moteur de vibration (shake_sensor) via une sortie GPIO.
    Inspiré du code CrowPi d'origine utilisant OutputDevice sur le pin 27.
    """

    def __init__(self, pin: int = 27):
        self.pin = pin
        self._device: Optional[OutputDevice] = OutputDevice(self.pin)

    def on(self) -> None:
        """Active la vibration en continu."""
        if self._device is not None:
            self._device.on()

    def off(self) -> None:
        """Désactive la vibration."""
        if self._device is not None:
            self._device.off()

    def pulse(self, duration_ms: int) -> None:
        """
        Active la vibration pendant une durée (ms), puis l'arrête.
        Bloquant, mais la durée est généralement courte.
        """
        if self._device is None:
            return

        try:
            duration = max(0, int(duration_ms))
        except (TypeError, ValueError):
            duration = 0

        if duration <= 0:
            return

        self._device.on()
        time.sleep(duration / 1000.0)
        self._device.off()


vibration = Vibration()

