import time

import smbus2


class LightSensor:
    def __init__(self, address=0x5C, bus=1):
        # Adresse I2C du capteur de lumière
        self.address = address
        self.bus_id = bus

        # Constantes issues de la datasheet / code d'origine
        self.POWER_DOWN = 0x00  # No active state
        self.POWER_ON = 0x01  # Power on
        self.RESET = 0x07  # Reset data register value

        # Modes de mesure
        # Start measurement at 1lx resolution. Time typically 120ms
        self.ONE_TIME_HIGH_RES_MODE_1 = 0x20

        self._last_lux = None
        self._last_read = 0

    def _convert_to_number(self, data):
        """
        Convertit 2 octets en valeur de luminosité (lux).
        Formule issue du code CrowPi d'origine.
        """
        return (data[1] + (256 * data[0])) / 1.2

    def read(self):
        """
        Lecture de la luminosité en lux.
        Utilise un petit cache pour éviter de sur-solliciter le bus I2C.
        """
        now = time.time()

        # Cache ~0.2 s
        if now - self._last_read < 0.2:
            return self._last_lux

        try:
            bus = smbus2.SMBus(self.bus_id)
            # Lecture en mode "one time high res"
            data = bus.read_i2c_block_data(
                self.address,
                self.ONE_TIME_HIGH_RES_MODE_1
            )
            lux = self._convert_to_number(data)

            self._last_lux = lux
            self._last_read = now
        except Exception:
            # En cas d'erreur I2C, on renvoie la dernière valeur connue
            pass

        return self._last_lux


lightsensor = LightSensor()

