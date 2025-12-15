import os
import threading
import typing as _t

import pygame


class MusicManager:
    """
    Gestion centralisée des musiques / sons via pygame.mixer.

    - Musiques (mp3, etc.) via pygame.mixer.music
    - Effets sonores (wav) via pygame.mixer.Sound
    - Génération simple de notes (sinus) pour le bloc "joue la note"
    """

    def __init__(self, sound_dir: str):
        self.sound_dir = sound_dir
        self._init_lock = threading.Lock()
        self._initialized = False

        self._sounds: dict[str, pygame.mixer.Sound] = {}

        # Mapping noms de notes (en français ou notation latine simplifiée)
        # vers des fréquences en Hz (gamme autour de C4).
        self._note_freqs: dict[str, float] = {
            # Octave "4" (centrale)
            "do": 261.63,
            "re": 293.66,
            "mi": 329.63,
            "fa": 349.23,
            "sol": 392.00,
            "la": 440.00,
            "si": 493.88,
            # Octave au-dessus (~5)
            "do2": 523.25,
            "re2": 587.33,
            "mi2": 659.25,
            "fa2": 698.46,
            "sol2": 783.99,
            "la2": 880.00,
            "si2": 987.77,
        }

    def _ensure_init(self) -> None:
        if self._initialized:
            return
        with self._init_lock:
            if self._initialized:
                return
            pygame.mixer.init(frequency=44100, size=-16, channels=2)
            self._initialized = True

    # --- Utils pour fichiers ---

    def _full_path(self, name: str) -> str:
        return os.path.join(self.sound_dir, name)

    def list_files(self) -> dict[str, _t.List[str]]:
        """
        Retourne les fichiers disponibles, séparés en:
        - musics: extensions .mp3, .ogg
        - sounds: extensions .wav, .ogg
        """
        musics: list[str] = []
        sounds: list[str] = []

        try:
            for entry in os.listdir(self.sound_dir):
                lower = entry.lower()
                if lower.endswith(".mp3") or lower.endswith(".ogg"):
                    musics.append(entry)
                if lower.endswith(".wav") or lower.endswith(".ogg"):
                    sounds.append(entry)
        except Exception:
            pass

        musics.sort()
        sounds.sort()
        return {"musics": musics, "sounds": sounds}

    # --- API musiques / sons ---

    def play_music(self, name: str) -> None:
        """
        Joue une musique (fichier long, mp3/ogg).
        """
        self._ensure_init()
        path = self._full_path(name)
        if not os.path.isfile(path):
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.play()
        except Exception:
            pass

    def stop_music(self) -> None:
        self._ensure_init()
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def _get_sound(self, name: str) -> _t.Optional[pygame.mixer.Sound]:
        self._ensure_init()
        if name in self._sounds:
            return self._sounds[name]

        path = self._full_path(name)
        if not os.path.isfile(path):
            return None
        try:
            snd = pygame.mixer.Sound(path)
            self._sounds[name] = snd
            return snd
        except Exception:
            return None

    def play_sound(self, name: str) -> None:
        """
        Joue un effet sonore (wav/ogg court).
        """
        snd = self._get_sound(name)
        if snd is None:
            return
        try:
            snd.play()
        except Exception:
            pass

    # --- Notes (générées) ---

    @staticmethod
    def _normalize_note_name(name: str) -> str:
        n = name.strip().lower()
        # Gestion minimale des accents pour "ré"
        n = n.replace("é", "e").replace("è", "e").replace("ê", "e")
        return n

    def play_note(self, name: str, duration_ms: int) -> None:
        """
        Génère une note simple (sinus) sur la durée donnée.
        Implémentation très basique, suffisante pour des bips.
        """
        self._ensure_init()

        key = self._normalize_note_name(name)
        freq = self._note_freqs.get(key)
        if freq is None:
            return

        try:
            duration_ms = int(duration_ms)
        except (TypeError, ValueError):
            duration_ms = 500
        if duration_ms <= 0:
            return

        # Génération d'une onde sinusoïdale 16 bits mono
        sample_rate = 44100
        duration_s = duration_ms / 1000.0
        sample_count = int(sample_rate * duration_s)
        if sample_count <= 0:
            return

        import math
        import array

        amplitude = 16000
        buf = array.array("h")
        for i in range(sample_count):
            t = i / sample_rate
            value = int(amplitude * math.sin(2 * math.pi * freq * t))
            buf.append(value)

        try:
            sound = pygame.mixer.Sound(buffer=buf.tobytes())
            sound.play()
        except Exception:
            pass


SOUND_DIR = os.path.join(
    os.path.dirname(__file__),
    "ressources",
    "sound",
)

music_manager = MusicManager(SOUND_DIR)
