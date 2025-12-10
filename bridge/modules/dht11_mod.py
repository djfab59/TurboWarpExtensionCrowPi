import Adafruit_DHT
import time

class DHT11:
    def __init__(self, pin=4):
        self.sensor = Adafruit_DHT.DHT11
        self.pin = pin
        self._last_temp = None
        self._last_humidity = None
        self._last_read = 0

    def read(self):
        """
        Lecture avec cache (DHT11 est LENT et fragile)
        """
        now = time.time()

        # Cache 2 secondes minimum
        if now - self._last_read < 2:
            return self._last_temp, self._last_humidity

        humidity, temperature = Adafruit_DHT.read_retry(
            self.sensor,
            self.pin
        )

        if humidity is not None and temperature is not None:
            self._last_temp = temperature
            self._last_humidity = humidity
            self._last_read = now

        return self._last_temp, self._last_humidity
    
dht11 = DHT11(pin=4)