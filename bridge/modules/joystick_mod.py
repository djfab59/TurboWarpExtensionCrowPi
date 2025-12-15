import spidev


class Joystick:
    """
    Lecture du joystick analogique CrowPi via MCP3008.

    On récupère uniquement les valeurs brutes X/Y (0–1023).
    La logique de “zone morte” et de directions (← → ↑ ↓)
    sera gérée côté extension JavaScript.
    """

    def __init__(self, x_channel=1, y_channel=0):
        self.x_channel = x_channel
        self.y_channel = y_channel

        # SPI MCP3008
        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 1_000_000

    def _read_channel(self, channel: int) -> int:
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def read(self):
        """
        Retourne un tuple (x, y) avec les valeurs brutes ADC (0–1023).
        """
        x = self._read_channel(self.x_channel)
        y = self._read_channel(self.y_channel)
        return x, y


joystick = Joystick()

