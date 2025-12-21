import time
import threading
from collections import deque

try:
    from gpiozero import InputDevice
except Exception:
    # Permet d'importer le module sur une machine sans GPIO
    InputDevice = None


class IRSensor:
    """
    Décodage de la télécommande IR CrowPi (protocole type NEC) basé sur les
    fronts (mesure de durées), inspiré de `test.py`.

    Objectif : éviter le décodage "au timing" à la volée dans step(), trop
    sensible au scheduling. On lance un thread qui écoute les changements
    d'état et reconstruit les trames en continu, puis step() dépile les events.
    """

    def __init__(
        self,
        pin: int = 20,
        sample_interval_s: float = 0.0002,
        frame_timeout_s: float = 0.12,
        queue_maxlen: int = 32,
        emit_repeats: bool = False,
    ):
        self.pin = pin
        self.sample_interval_s = sample_interval_s
        self.frame_timeout_s = frame_timeout_s
        self.emit_repeats = bool(emit_repeats)
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

        self._queue = deque(maxlen=int(queue_maxlen))
        self._queue_lock = threading.Lock()

        self._stop_event = threading.Event()
        self._thread = None

        self._decoder_state = "IDLE"
        self._bits = []
        self._last_command = None
        self._last_frame_time_s = 0.0

        if self.device is not None:
            self._thread = threading.Thread(
                target=self._reader_loop,
                name="IRSensorReader",
                daemon=True,
            )
            self._thread.start()

    def _value(self) -> int:
        if self.device is None:
            return 1
        try:
            return int(self.device.value)
        except Exception:
            return 1

    @staticmethod
    def _in_range(value_us: int, min_us: int, max_us: int) -> bool:
        return min_us <= value_us <= max_us

    def _reset_decoder(self) -> None:
        self._decoder_state = "IDLE"
        self._bits = []

    def _push_event(self, raw_code: int) -> None:
        name = self.key_names.get(raw_code)
        if not name:
            return
        with self._queue_lock:
            self._queue.append((raw_code, name))

    def _finalize_frame(self) -> None:
        if len(self._bits) < 32:
            return

        data = [0, 0, 0, 0]
        for i in range(32):
            if self._bits[i]:
                data[i // 8] |= 1 << (i % 8)

        addr, addr_inv, cmd, cmd_inv = data
        if (addr ^ addr_inv) & 0xFF != 0xFF:
            return
        if (cmd ^ cmd_inv) & 0xFF != 0xFF:
            return

        self._last_command = cmd
        self._push_event(cmd)

    def _process_segment(self, level: int, duration_us: int) -> None:
        """
        Reçoit des segments (niveau stable + durée) et avance l'automate NEC.

        level: 0 (LOW) ou 1 (HIGH) sur le pin IR
        duration_us: durée (µs) pendant laquelle ce niveau est resté stable
        """
        # Filtre très court (glitch / jitter)
        if duration_us < 80:
            return

        # Fenêtres tolérantes (polling -> timestamps un peu jittery)
        leader_low = (7500, 11500)      # ~9000us
        leader_high = (3000, 6000)      # ~4500us
        repeat_high = (1500, 3500)      # ~2250us
        bit_low = (200, 900)            # ~560us
        bit_high_minmax = (200, 2500)   # 0:~560us / 1:~1690us
        bit_one_threshold = 1000        # seuil simple entre 0 et 1

        if self._decoder_state == "IDLE":
            if level == 0 and self._in_range(duration_us, *leader_low):
                self._decoder_state = "LEADER_HIGH"
            return

        if self._decoder_state == "LEADER_HIGH":
            if level != 1:
                self._reset_decoder()
                return
            if self._in_range(duration_us, *leader_high):
                self._bits = []
                self._decoder_state = "BIT_LOW"
                return
            if self._in_range(duration_us, *repeat_high):
                self._decoder_state = "REPEAT_LOW"
                return
            self._reset_decoder()
            return

        if self._decoder_state == "REPEAT_LOW":
            # Repeat frame: leader(9ms low) + space(2.25ms high) + 560us low
            if level == 0 and self._in_range(duration_us, *bit_low):
                if self.emit_repeats and self._last_command is not None:
                    self._push_event(self._last_command)
            self._reset_decoder()
            return

        if self._decoder_state == "BIT_LOW":
            if level == 0 and self._in_range(duration_us, *bit_low):
                self._decoder_state = "BIT_HIGH"
                return
            self._reset_decoder()
            return

        if self._decoder_state == "BIT_HIGH":
            if level != 1 or not self._in_range(duration_us, *bit_high_minmax):
                self._reset_decoder()
                return

            bit = 1 if duration_us >= bit_one_threshold else 0
            self._bits.append(bit)

            if len(self._bits) >= 32:
                self._finalize_frame()
                self._reset_decoder()
                return

            self._decoder_state = "BIT_LOW"
            return

        self._reset_decoder()

    def _reader_loop(self) -> None:
        last_state = self._value()
        last_edge_ns = time.monotonic_ns()
        while not self._stop_event.is_set():
            state = self._value()
            now_ns = time.monotonic_ns()

            if state != last_state:
                duration_us = int((now_ns - last_edge_ns) / 1000)
                self._process_segment(last_state, duration_us)

                last_state = state
                last_edge_ns = now_ns
                self._last_frame_time_s = time.monotonic()
            else:
                # Si on attend une fin de trame et que ça traîne, reset
                if (
                    self._decoder_state != "IDLE"
                    and (time.monotonic() - self._last_frame_time_s) > self.frame_timeout_s
                ):
                    self._reset_decoder()

            time.sleep(self.sample_interval_s)

    def step(self):
        """
        Dépile un événement IR si disponible.

        Retourne (raw_code, name) ou (None, None) si rien.
        """
        with self._queue_lock:
            if not self._queue:
                return None, None
            return self._queue.popleft()

    def close(self) -> None:
        self._stop_event.set()


ir_sensor = IRSensor()
