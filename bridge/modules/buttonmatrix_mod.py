import time
import spidev


class ButtonMatrix:
    def __init__(self, key_channel=4):
        # Canal ADC utilisé par le clavier (0–7)
        self.key_channel = key_channel
        self.delay = 0.1

        self.adc_key_val = [
            30, 90, 160, 230,
            280, 330, 400, 470,
            530, 590, 650, 720,
            780, 840, 890, 960
        ]
        self.key = -1
        self.oldkey = -1
        self.num_keys = 16

        # Mapping “brut” (index 0–15 renvoyé par GetKeyNum)
        # vers un index logique (1–16) utilisé par l'application.
        # Cette table dépend du câblage physique de la matrice.
        self.indexes = {
            12: 1,
            13: 2,
            14: 3,
            15: 4,
            10: 5,
            9: 6,
            8: 7,
            11: 8,
            4: 9,
            5: 10,
            6: 11,
            7: 12,
            0: 13,
            1: 14,
            2: 15,
            3: 16
        }

        # SPI MCP3008
        self.spi = spidev.SpiDev()
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 1_000_000

    # ---------- Lecture matérielle ----------

    def read_channel(self, channel):
        # Lecture SPI depuis MCP3008
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def get_adc_value(self):
        return self.read_channel(self.key_channel)

    def get_key_num(self, adc_key_value):
        for num in range(0, 16):
            if adc_key_value < self.adc_key_val[num]:
                return num
        if adc_key_value >= self.num_keys:
            num = -1
            return num

    # ---------- API événementielle ----------

    def step(self):
        """
        Une “itération” de lecture :
        - front montant (nouvelle touche pressée)  -> retourne (raw, mapped, "down")
        - front descendant (touche relâchée)      -> retourne (raw, mapped, "up")
        - sinon                                   -> retourne (-1, -1, None)

        raw    : index brut (0–15) renvoyé par le driver
        mapped : index logique (1–16) après mapping
        """
        adc_key_value = self.get_adc_value()
        key = self.get_key_num(adc_key_value)

        if key != self.oldkey:
            # petite temporisation pour éviter les rebonds
            time.sleep(0.05)
            adc_key_value = self.get_adc_value()
            key = self.get_key_num(adc_key_value)

            if key != self.oldkey:
                previous = self.oldkey
                self.oldkey = key

                # Détection relâche : on passe d'une touche valide à -1
                if previous is not None and previous >= 0 and key == -1:
                    raw = int(previous)
                    mapped = int(self.indexes.get(raw, raw))
                    return raw, mapped, "up"

                # Détection appui : on passe à une touche valide
                if key is not None and key >= 0:
                    raw = int(key)
                    mapped = int(self.indexes.get(raw, raw))
                    return raw, mapped, "down"

        return -1, -1, None


button_matrix = ButtonMatrix()
