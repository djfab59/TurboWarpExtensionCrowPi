import time
from typing import Optional

from gpiozero import DistanceSensor


class UltrasonicSensor:
    def __init__(self, echo: int = 26, trigger: int = 16, max_distance: float = 5.0):
        # Capteur ultrason branché sur echo=26, trigger=16, comme dans le code CrowPi
        self.sensor = DistanceSensor(echo=echo, trigger=trigger, max_distance=max_distance)
        self._last_distance_cm: Optional[float] = None
        self._last_read = 0.0

    def read(self) -> Optional[float]:
        """
        Renvoie la distance en centimètres (float), ou None si la mesure échoue.
        Utilise un petit cache pour éviter de sur-solliciter le capteur.
        """
        now = time.time()
        # Cache 0.1 s
        if now - self._last_read < 0.1:
            return self._last_distance_cm

        try:
            # gpiozero.DistanceSensor.distance renvoie une valeur en mètres
            distance_m = self.sensor.distance
            distance_cm = distance_m * 100.0
            self._last_distance_cm = distance_cm
            self._last_read = now
        except Exception:
            # En cas d'erreur ou timeout, on renvoie la dernière valeur connue
            pass

        return self._last_distance_cm


ultrasonicsensor = UltrasonicSensor()

