import threading
import time
from typing import Any, Optional

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone

from bridge.modules.melodies import MELODIES


class Buzzer:
    def __init__(self, pin: int = 18):
        self.pin = pin
        # TonalBuzzer sera créé à la demande pour éviter les
        # artefacts sonores persistants. On le recrée après chaque OFF.
        self._buzzer: Optional[TonalBuzzer] = None
        self._melody_thread: Optional[threading.Thread] = None
        self._melody_stop = threading.Event()

    # ---------- Helpers ----------

    def _to_tone(self, value: Any) -> Optional[Tone]:
        """
        Convertit une valeur en Tone gpiozero.
        Accepte :
        - nom de note ("C4", "A5", etc.)
        - fréquence numérique (440, 261.6, ...)
        """
        if value is None:
            return None

        try:
            # Essaie directement (note ou fréquence numérique)
            return Tone(value)
        except Exception:
            # Dernière tentative : conversion en float
            try:
                return Tone(float(value))
            except Exception:
                return None

    def _ensure_buzzer(self) -> TonalBuzzer:
        """
        Crée l'instance TonalBuzzer au besoin.
        On évite de garder un PWM vivant trop longtemps.
        """
        if self._buzzer is None:
            self._buzzer = TonalBuzzer(self.pin)
        return self._buzzer

    def _stop_buzzer(self):
        """
        Arrête complètement le buzzer et libère les ressources PWM.
        Cela permet d'éviter le sifflement résiduel observé après OFF.
        """
        buz = self._buzzer
        if buz is not None:
            try:
                buz.stop()
            except Exception:
                pass
            try:
                buz.close()
            except Exception:
                pass
        self._buzzer = None

    # ---------- API simple ----------

    def on_freq(self, freq_hz: float) -> None:
        """Allume le buzzer à une fréquence donnée (Hz) jusqu'à extinction."""
        self.stop_melody()

        tone = self._to_tone(freq_hz)
        if tone is None:
            return
        buz = self._ensure_buzzer()
        buz.play(tone)

    def off(self) -> None:
        """Éteint le buzzer (et arrête toute mélodie)."""
        self.stop_melody()
        self._stop_buzzer()

    def play_note(self, note: Any, duration_ms: int) -> None:
        """
        Joue une note pendant une durée donnée (ms).
        Bloquant, mais durée généralement courte.
        """
        self.stop_melody()

        tone = self._to_tone(note)
        if tone is None:
            return

        buz = self._ensure_buzzer()
        buz.play(tone)
        time.sleep(max(0, duration_ms) / 1000.0)
        self._stop_buzzer()

    # ---------- Mélodies ----------

    def _run_melody(self, sequence):
        """Boucle interne exécutée dans un thread pour jouer une mélodie."""
        for item in sequence:
            # Vérifie au début de chaque étape si un arrêt a été demandé.
            if self._melody_stop.is_set():
                break

            if not isinstance(item, (tuple, list)) or len(item) != 2:
                continue

            note, duration_ms = item

            # Silence
            if note in (None, "-", "REST"):
                self._stop_buzzer()
                time.sleep(max(0, int(duration_ms)) / 1000.0)
                continue

            # Nouvelle vérification juste avant de (re)jouer un son afin
            # d'éviter de rallumer le buzzer après un OFF.
            if self._melody_stop.is_set():
                break

            tone = self._to_tone(note)
            if tone is None:
                continue

            buz = self._ensure_buzzer()
            buz.play(tone)
            time.sleep(max(0, int(duration_ms)) / 1000.0)

        # Fin de mélodie
        self._stop_buzzer()

    def play_melody(self, name: str) -> None:
        """
        Lance la lecture d'une mélodie par son nom.
        La lecture se fait dans un thread dédié pour ne pas bloquer Flask.
        """
        # Arrête proprement toute mélodie en cours
        self.stop_melody()
        sequence = MELODIES.get(name)
        if not sequence:
            return

        self._melody_stop.clear()
        self._melody_thread = threading.Thread(
            target=self._run_melody,
            args=(sequence,),
            daemon=True,
        )
        self._melody_thread.start()

    def stop_melody(self) -> None:
        """Demande l'arrêt de la mélodie en cours (si présente)."""
        self._melody_stop.set()
        thread = self._melody_thread
        if thread is not None and thread.is_alive():
            # Laisse au thread un peu plus de temps pour s'arrêter
            # et ne pas rallumer le buzzer juste après un OFF.
            thread.join(timeout=1.0)
        self._melody_thread = None


buzzer = Buzzer()
