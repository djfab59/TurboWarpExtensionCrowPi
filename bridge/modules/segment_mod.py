from typing import Optional

from Adafruit_LED_Backpack import SevenSegment


class SegmentDisplay:
    """
    Wrapper autour du module Adafruit SevenSegment pour un afficheur 4 digits.
    Fournit des méthodes simples pour l'initialisation, l'affichage de nombres,
    la gestion des points / deux-points et de la luminosité.
    """

    def __init__(self, address: int = 0x70):
        self.address = address
        self._segment: Optional[SevenSegment.SevenSegment] = SevenSegment.SevenSegment(
            address=self.address
        )
        self._initialized = False

    # ---------- Helpers ----------

    def _ensure_init(self) -> None:
        if not self._initialized:
            self._segment.begin()
            self._segment.clear()
            self._segment.write_display()
            self._initialized = True

    # ---------- API publique ----------

    def init(self) -> None:
        """Initialise le 7-segments (idempotent)."""
        self._ensure_init()

    def clear(self) -> None:
        """Efface complètement l'affichage."""
        self._ensure_init()
        self._segment.clear()
        self._segment.write_display()

    def display_number(self, value) -> None:
        """
        Affiche un nombre entre 0 et 9999 sur les 4 digits.
        Valeurs hors plage sont clampées.
        """
        self._ensure_init()
        try:
            n = int(value)
        except (TypeError, ValueError):
            n = 0

        if n < 0:
            n = 0
        if n > 9999:
            n = 9999

        s = f"{n:04d}"
        self._segment.print_number_str(s)
        self._segment.write_display()

    def set_digit(self, position: int, digit) -> None:
        """
        Écrit un chiffre (0–9) sur un digit (1–4).
        position : 1 = digit le plus à gauche, 4 = le plus à droite.
        """
        self._ensure_init()

        try:
            pos = int(position)
        except (TypeError, ValueError):
            return

        try:
            d = int(digit)
        except (TypeError, ValueError):
            return

        if not (1 <= pos <= 4):
            return
        if not (0 <= d <= 9):
            return

        index = pos - 1
        self._segment.set_digit(index, d)
        self._segment.write_display()

    def set_decimal_point(self, position: int, on: bool) -> None:
        """
        Active ou désactive le point du digit (1–4).
        """
        self._ensure_init()

        try:
            pos = int(position)
        except (TypeError, ValueError):
            return

        if not (1 <= pos <= 4):
            return

        index = pos - 1
        self._segment.set_decimal(index, bool(on))
        self._segment.write_display()

    def set_colon(self, on: bool) -> None:
        """Active ou désactive les deux-points centraux."""
        self._ensure_init()
        self._segment.set_colon(bool(on))
        self._segment.write_display()

    def set_digit_raw(self, position: int, bitmask: int) -> None:
        """
        Écrit une valeur brute (bitmask 0–255) sur un digit (1–4).
        """
        self._ensure_init()

        try:
            pos = int(position)
            mask = int(bitmask)
        except (TypeError, ValueError):
            return

        if not (1 <= pos <= 4):
            return

        mask &= 0xFF
        index = pos - 1
        self._segment.set_digit_raw(index, mask)
        self._segment.write_display()

    def set_brightness(self, level: int) -> None:
        """
        Règle la luminosité de l'afficheur (0–15).
        """
        self._ensure_init()

        try:
            val = int(level)
        except (TypeError, ValueError):
            return

        if val < 0:
            val = 0
        if val > 15:
            val = 15

        # Méthode héritée de HT16K33
        self._segment.set_brightness(val)


segment_display = SegmentDisplay()

