import threading
import time
from typing import Dict, List, Tuple, Optional

from elecrow_ws281x import PixelStrip, Color

from bridge.modules.animations import ANIMATIONS


class LedMatrix:
    def __init__(self, led_count: int = 64, pin: int = 10):
        # Matrice 8x8 sur bande WS2812 (64 LEDs)
        self.led_count = led_count
        self.width = 8
        self.height = 8

        self.strip = PixelStrip(self.led_count, pin)
        self.strip.begin()

        self._anim_thread: Optional[threading.Thread] = None
        self._anim_stop = threading.Event()

    # ---------- Helpers ----------

    def _index_from_xy(self, x: int, y: int) -> Optional[int]:
        """
        Convertit des coordonnées (x, y) en index 0–63.
        x, y sont attendus en 1–8 depuis l'API, on les convertit en 0–7.
        """
        try:
            x = int(x)
            y = int(y)
        except (TypeError, ValueError):
            return None

        # Conversion 1-based -> 0-based
        x -= 1
        y -= 1

        if not (0 <= x < self.width and 0 <= y < self.height):
            return None

        return y * self.width + x

    @staticmethod
    def _color_from_name(name: str) -> Tuple[int, int, int]:
        """
        Convertit un nom de couleur simple en (r, g, b).
        """
        if not isinstance(name, str):
            return 255, 255, 255

        name = name.strip().lower()
        mapping: Dict[str, Tuple[int, int, int]] = {
            "rouge": (255, 0, 0),
            "red": (255, 0, 0),
            "vert": (0, 255, 0),
            "green": (0, 255, 0),
            "bleu": (0, 0, 255),
            "blue": (0, 0, 255),
            "blanc": (255, 255, 255),
            "white": (255, 255, 255),
            "jaune": (255, 255, 0),
            "yellow": (255, 255, 0),
            "cyan": (0, 255, 255),
            "magenta": (255, 0, 255),
            "rose": (255, 105, 180),
            "orange": (255, 165, 0),
            "violet": (128, 0, 128),
            "noir": (0, 0, 0),
            "black": (0, 0, 0),
        }
        return mapping.get(name, (255, 255, 255))

    def _set_pixel(self, index: int, r: int, g: int, b: int) -> None:
        if index is None or not (0 <= index < self.led_count):
            return
        self.strip.setPixelColor(index, Color(r, g, b))

    # ---------- API simple ----------

    def clear(self) -> None:
        """Éteint toutes les LEDs."""
        self.strip.fill(0, 0, 0)
        self.strip.show()

    def set_pixel_named(self, x: int, y: int, color_name: str) -> None:
        """Allume un pixel (x, y) avec une couleur nommée."""
        index = self._index_from_xy(x, y)
        r, g, b = self._color_from_name(color_name)
        self._set_pixel(index, r, g, b)
        self.strip.show()

    def set_pixel_rgb(self, x: int, y: int, r: int, g: int, b: int) -> None:
        """Allume un pixel (x, y) avec des composantes RGB."""
        index = self._index_from_xy(x, y)
        try:
            r = int(r)
            g = int(g)
            b = int(b)
        except (TypeError, ValueError):
            return

        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        self._set_pixel(index, r, g, b)
        self.strip.show()

    def clear_pixel(self, x: int, y: int) -> None:
        """Éteint un pixel (x, y)."""
        index = self._index_from_xy(x, y)
        self._set_pixel(index, 0, 0, 0)
        self.strip.show()

    def fill_named(self, color_name: str) -> None:
        """Remplit la matrice avec une couleur nommée."""
        r, g, b = self._color_from_name(color_name)
        self.strip.fill(r, g, b)
        self.strip.show()

    # ---------- Animations ----------

    def _run_animation(
        self,
        frames: List[Dict[str, object]],
        override_rgb: Optional[Tuple[int, int, int]] = None
    ) -> None:
        for frame in frames:
            if self._anim_stop.is_set():
                break

            pixels = frame.get("pixels", [])
            color = frame.get("color", (255, 255, 255))
            duration = int(frame.get("duration", 200))

            if override_rgb is not None:
                r, g, b = override_rgb
            else:
                try:
                    r, g, b = color
                except Exception:
                    r, g, b = 255, 255, 255

            # Efface tout
            self.strip.fill(0, 0, 0)

            # Allume uniquement les pixels de la frame
            for idx in pixels:
                try:
                    idx = int(idx)
                except (TypeError, ValueError):
                    continue
                self._set_pixel(idx, r, g, b)

            self.strip.show()
            time.sleep(max(0, duration) / 1000.0)

    def play_animation(self, name: str, color_name: Optional[str] = None) -> None:
        """Lance une animation par son nom, avec couleur optionnelle, dans un thread dédié."""
        self.stop_animation()

        frames = ANIMATIONS.get(str(name).lower())
        if not frames:
            return

        override_rgb = None
        if color_name is not None:
            override_rgb = self._color_from_name(color_name)

        self._anim_stop.clear()
        self._anim_thread = threading.Thread(
            target=self._run_animation,
            args=(frames, override_rgb),
            daemon=True,
        )
        self._anim_thread.start()

    def stop_animation(self) -> None:
        """Arrête l'animation en cours (si présente)."""
        self._anim_stop.set()
        thread = self._anim_thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=0.1)
        self._anim_thread = None
        self._anim_stop.clear()


ledmatrix = LedMatrix()
