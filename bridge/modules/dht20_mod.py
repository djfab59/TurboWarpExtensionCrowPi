import time
import smbus2

class DHT20:
    def __init__(self, address=0x38, bus=1):
        self.address = address
        self.bus_id = bus
        self._last_temp = None
        self._last_humidity = None
        self._last_read = 0

    def read(self):
        """
        Lecture avec cache via I2C (DHT20)
        """
        now = time.time()

        # Cache 2 secondes minimum
        if now - self._last_read < 2:
            return self._last_temp, self._last_humidity

        try:
            i2cbus = smbus2.SMBus(self.bus_id)

            # Réveil / vérification du capteur
            time.sleep(0.5)
            data = i2cbus.read_i2c_block_data(self.address, 0x71, 1)
            if (data[0] | 0x08) == 0:
                # Erreur d'initialisation, on retourne la dernière valeur connue
                return self._last_temp, self._last_humidity

            # Lancement mesure
            i2cbus.write_i2c_block_data(self.address, 0xac, [0x33, 0x00])
            time.sleep(0.1)

            # Lecture résultats (7 octets)
            data = i2cbus.read_i2c_block_data(self.address, 0x71, 7)

            # Température
            traw = ((data[3] & 0x0F) << 16) + (data[4] << 8) + data[5]
            temperature = 200 * float(traw) / (2 ** 20) - 50

            # Humidité
            hraw = ((data[3] & 0xF0) >> 4) + (data[1] << 12) + (data[2] << 4)
            humidity = 100 * float(hraw) / (2 ** 20)

            self._last_temp = temperature
            self._last_humidity = humidity
            self._last_read = now
        except Exception:
            # En cas d'erreur I2C, on renvoie les dernières valeurs valides
            pass

        return self._last_temp, self._last_humidity

dht20 = DHT20()
