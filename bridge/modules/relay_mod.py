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
        # On ne crée pas tout de suite l'OutputDevice pour éviter
        # un "clac" du relais au démarrage de run.py si on ne
        # l'utilise pas. Il sera créé à la première utilisation.
        self._device: Optional[OutputDevice] = None

    def _ensure_device(self) -> Optional[OutputDevice]:
        """
        Crée l'OutputDevice à la demande.
        active_high=False pour que .on() mette la broche à LOW (relais actif),
        comme dans l'exemple d'origine où GPIO.LOW active le relais.
        """
        if self._device is None:
            self._device = OutputDevice(
                self.pin,
                active_high=False,
                initial_value=False
            )
        return self._device

    def on(self) -> None:
        """Active le relais."""
        dev = self._ensure_device()
        if dev is not None:
            dev.on()

    def off(self) -> None:
        """Désactive le relais."""
        dev = self._ensure_device()
        if dev is not None:
            dev.off()

    def pulse(self, duration_ms: int) -> None:
        """
        Active le relais pendant une durée (ms), puis le désactive.
        Bloquant, mais la durée est généralement courte.
        """
        if self._device is None:
            self._ensure_device()
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
