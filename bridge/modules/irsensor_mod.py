import time

try:
    from gpiozero import InputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    InputDevice = None


class IRSensor:
    """
    Décodage simple de la télécommande IR CrowPi (protocole type NEC).

    On expose une API step() qui essaie de décoder une trame complète :
    - si aucune trame valide n'est détectée : retourne (None, None)
    - sinon : retourne (raw_code, name) où :
        raw_code : valeur entière (octet de données, ex 0x45)
        name     : nom logique ("CH_MINUS", "CH", "CH_PLUS", "NUM_0", etc.)
    """

    def __init__(self, pin: int = 20):
        self.pin = pin
        if InputDevice is not None:
            try:
                self.device = InputDevice(pin)
            except Exception:
                self.device = None
        else:
            self.device = None

        # Mapping codes -> noms logiques (issus de Remote_controller_copy.py)
        self.key_names = {
            0x45: "CH_MINUS",
            0x46: "CH",
            0x47: "CH_PLUS",
            0x44: "PREV",
            0x40: "NEXT",
            0x43: "PLAY_PAUSE",
            0x07: "PREV_TRACK",
            0x15: "NEXT_TRACK",
            0x09: "EQ",
            0x16: "NUM_0",
            0x19: "HUNDRED_PLUS",
            0x0D: "TWOHUNDRED_PLUS",
            0x0C: "NUM_1",
            0x18: "NUM_2",
            0x5E: "NUM_3",
            0x08: "NUM_4",
            0x1C: "NUM_5",
            0x5A: "NUM_6",
            0x42: "NUM_7",
            0x52: "NUM_8",
            0x4A: "NUM_9",
        }

    def _value(self) -> int:
        if self.device is None:
            return 1
        try:
            return int(self.device.value)
        except Exception:
            return 1

    def _decode_once(self):
        """
        Tentative de décodage d'une trame IR.
        Retourne raw code (data[2]) ou None.
        Implémentation adaptée de Remote_controller_copy.py (boucles de timing).
        """
        if self._value() != 0:
            return None

        count = 0
        while self._value() == 0 and count < 200:
            count += 1
            time.sleep(0.00006)

        count = 0
        while self._value() == 1 and count < 80:
            count += 1
            time.sleep(0.00006)

        idx = 0
        cnt = 0
        data = [0, 0, 0, 0]
        for _ in range(32):
            count = 0
            while self._value() == 0 and count < 15:
                count += 1
                time.sleep(0.00006)

            count = 0
            while self._value() == 1 and count < 40:
                count += 1
                time.sleep(0.00006)

            if count > 8:
                data[idx] |= 1 << cnt
            if cnt == 7:
                cnt = 0
                idx += 1
            else:
                cnt += 1

        if data[0] + data[1] == 0xFF and data[2] + data[3] == 0xFF:
            raw = data[2]
            return raw

        return None

    def step(self):
        """
        Essaie de lire une trame IR complète.
        Retourne (raw_code, name) ou (None, None) si rien de valide.
        """
        raw = self._decode_once()
        if raw is None:
            return None, None

        name = self.key_names.get(raw)
        return raw, name


ir_sensor = IRSensor()
