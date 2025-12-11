import time
from typing import Optional

from gpiozero import OutputDevice


class Relay:
    """
    Contrôle d'un relais via une sortie GPIO.
    Inspiré du code CrowPi d'origine utilisant GPIO.BCM 21.
    """

    def __init__(self, pin: int = 21):
        self.pin = pin
        # active_high=False pour que .on() mette la broche à l'état BAS (LOW),
        # comme dans l'exemple d'origine où GPIO.LOW active le relais.
        self._device: Optional[OutputDevice] = OutputDevice(
            self.pin,
            active_high=False,
            initial_value=False
        )

    def on(self) -> None:
        """Active le relais."""
        if self._device is not None:
            self._device.on()

    def off(self) -> None:
        """Désactive le relais."""
        if self._device is not None:
            self._device.off()

    def pulse(self, duration_ms: int) -> None:
        """
        Active le relais pendant une durée (ms), puis le désactive.
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


relay = Relay()

