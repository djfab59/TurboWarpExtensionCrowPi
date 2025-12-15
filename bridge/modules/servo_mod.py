from typing import Optional

try:
    from gpiozero import Servo
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    Servo = None


class ServoController:
    """
    Gestion d'un ou plusieurs servos.

    - API basée sur des angles 0–180 côté Flask/JS.
    - Conversion interne en position gpiozero (-1.0 à +1.0).
    """

    def __init__(self):
        # Mapping servo_id -> (pin, Servo instance)
        # Par défaut, on mappe l'ID "1" sur la broche 19,
        # comme dans l'exemple Servo_wave.py
        self._config = {
            1: 19
        }
        self._servos: dict[int, Optional["Servo"]] = {}
        self._angles: dict[int, float] = {}

    def _ensure_servo(self, servo_id: int) -> Optional["Servo"]:
        if Servo is None:
            return None

        pin = self._config.get(servo_id)
        if pin is None:
            return None

        if servo_id not in self._servos or self._servos[servo_id] is None:
            try:
                self._servos[servo_id] = Servo(pin)
            except Exception:
                self._servos[servo_id] = None

        return self._servos[servo_id]

    @staticmethod
    def _angle_to_position(angle: float) -> float:
        """
        Convertit un angle 0–180° en position Servo (-1.0 à +1.0).
        0°  -> -1.0 (min)
        90° ->  0.0 (centre)
        180°-> +1.0 (max)
        """
        angle = max(0.0, min(180.0, float(angle)))
        return (angle / 90.0) - 1.0

    @staticmethod
    def _position_to_angle(pos: float) -> float:
        """
        Conversion inverse. Clamp pour éviter les petites dérives.
        """
        pos = max(-1.0, min(1.0, float(pos)))
        return (pos + 1.0) * 90.0

    def set_angle(self, servo_id: int, angle: float) -> None:
        servo = self._ensure_servo(servo_id)
        if servo is None:
            return

        pos = self._angle_to_position(angle)
        try:
            servo.value = pos
            self._angles[servo_id] = float(angle)
        except Exception:
            pass

    def set_position(self, servo_id: int, position: str) -> None:
        """
        position: "min", "center", "max"
        """
        mapping = {
            "min": 0.0,
            "centre": 90.0,
            "center": 90.0,
            "mid": 90.0,
            "max": 180.0
        }
        angle = mapping.get(position.lower())
        if angle is None:
            return
        self.set_angle(servo_id, angle)

    def get_angle(self, servo_id: int) -> Optional[float]:
        if servo_id in self._angles:
            return self._angles[servo_id]

        servo = self._ensure_servo(servo_id)
        if servo is None:
            return None

        try:
            if servo.value is None:
                return None
            return self._position_to_angle(servo.value)
        except Exception:
            return None


servo_controller = ServoController()

