import math
import time
from typing import Optional

try:
    from gpiozero import OutputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    OutputDevice = None


class StepMotor:
    """
    Contrôle du moteur pas à pas (Lucky_turntable) via 4 sorties GPIO.

    Séquence issue de Lucky_turntable.py, avec ajout de la notion de sens
    (horaire / anti-horaire) et d'un API en degrés / pas.
    """

    def __init__(self):
        self._a: Optional[OutputDevice] = None
        self._b: Optional[OutputDevice] = None
        self._c: Optional[OutputDevice] = None
        self._d: Optional[OutputDevice] = None
        # Intervalle de base entre demi-pas (reprend la valeur d'origine)
        self._base_interval = 0.0011
        self.interval = self._base_interval
        # Compteur logique de pas (relatif) depuis le dernier reset.
        # Sens "cw" positif, "ccw" négatif.
        self._logical_steps = 0

    def _ensure_pins(self) -> bool:
        if OutputDevice is None:
            return False

        if self._a is None:
            try:
                self._a = OutputDevice(5)
                self._b = OutputDevice(6)
                self._c = OutputDevice(13)
                self._d = OutputDevice(25)
                self._a.off()
                self._b.off()
                self._c.off()
                self._d.off()
            except Exception:
                self._a = self._b = self._c = self._d = None
                return False

        return all(pin is not None for pin in (self._a, self._b, self._c, self._d))

    # --- Séquence de pas (demi-pas) ---

    def _set_speed(self, speed: float):
        """
        Ajuste l'intervalle en fonction d'un facteur de vitesse.
        speed ~1.0 => vitesse "normale"
        speed >1.0 => plus rapide, speed<1.0 => plus lent
        """
        try:
            speed = float(speed)
        except (TypeError, ValueError):
            speed = 1.0

        # Clamp pour éviter des valeurs extrêmes
        if speed <= 0:
            speed = 0.1
        if speed > 20:
            speed = 20.0

        self.interval = self._base_interval / speed

    def _step1(self):
        self._d.on()
        time.sleep(self.interval)
        self._d.off()

    def _step2(self):
        self._d.on()
        self._c.on()
        time.sleep(self.interval)
        self._d.off()
        self._c.off()

    def _step3(self):
        self._c.on()
        time.sleep(self.interval)
        self._c.off()

    def _step4(self):
        self._b.on()
        self._c.on()
        time.sleep(self.interval)
        self._b.off()
        self._c.off()

    def _step5(self):
        self._b.on()
        time.sleep(self.interval)
        self._b.off()

    def _step6(self):
        self._a.on()
        self._b.on()
        time.sleep(self.interval)
        self._a.off()
        self._b.off()

    def _step7(self):
        self._a.on()
        time.sleep(self.interval)
        self._a.off()

    def _step8(self):
        self._d.on()
        self._a.on()
        time.sleep(self.interval)
        self._d.off()
        self._a.off()

    def _sequence_forward(self):
        self._step1()
        self._step2()
        self._step3()
        self._step4()
        self._step5()
        self._step6()
        self._step7()
        self._step8()

    def _sequence_backward(self):
        self._step8()
        self._step7()
        self._step6()
        self._step5()
        self._step4()
        self._step3()
        self._step2()
        self._step1()

    # --- API publique ---

    def turn_steps(self, steps: int, direction: str = "cw", speed: float = 1.0):
        """
        Fait tourner le moteur d'un nombre de pas "logiques".
        Chaque pas logique correspond à une séquence complète de 8 demi-pas.
        direction: "cw" (horaire) ou "ccw" (anti-horaire)
        """
        if not self._ensure_pins():
            return

        try:
            steps = int(steps)
        except (TypeError, ValueError):
            return

        if steps <= 0:
            return

        self._set_speed(speed)

        forward = direction != "ccw"
        for _ in range(steps):
            if forward:
                self._sequence_forward()
            else:
                self._sequence_backward()

        # Mise à jour de la position logique
        if forward:
            self._logical_steps += steps
        else:
            self._logical_steps -= steps

    def turn_degrees(self, degrees: float, direction: str = "cw", speed: float = 1.0):
        """
        Tourne le moteur d'un certain nombre de degrés.
        Approximation basée sur 512 pas logiques pour 360° (comme dans l'exemple).
        """
        try:
            degrees = float(degrees)
        except (TypeError, ValueError):
            return

        if degrees == 0:
            return

        # Signe du mouvement = sens, valeur absolue pour les pas
        if degrees < 0:
            degrees = abs(degrees)
            direction = "ccw" if direction == "cw" else "cw"

        steps = int(round(512.0 * degrees / 360.0))
        if steps <= 0:
            steps = 1

        self.turn_steps(steps, direction=direction, speed=speed)

    # --- Position logique (relative) ---

    def reset_position(self) -> None:
        """Réinitialise la position logique à 0 pas."""
        self._logical_steps = 0

    def get_position_degrees(self) -> float:
        """
        Retourne la position logique estimée en degrés.
        512 pas logiques ~ 360° comme dans l'exemple d'origine.
        """
        return (self._logical_steps * 360.0) / 512.0


stepmotor = StepMotor()
