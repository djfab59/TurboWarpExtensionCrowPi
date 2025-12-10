import time
from crowpi_lcd import LCDModule as _LCD

class LCD:
    def __init__(self):
        self.lcd = _LCD()

    def on(self):
        self.lcd.on()

    def off(self):
        self.lcd.off()

    def clear(self):
        self.lcd.clear()
        time.sleep(0.02)

    def write(self, text):
        self.on()
        self.lcd.write(text)
        time.sleep(0.02)

    def write_line(self, line, text):
        if line not in (1, 2):
            return
        self.on()
        self.lcd.lcd.display_string(text[:16], line)
        time.sleep(0.02)

    def write_both(self, l1, l2):
        self.on()
        self.lcd.lcd.clear_display()
        time.sleep(0.02)
        self.lcd.lcd.display_string(l1[:16], 1)
        self.lcd.lcd.display_string(l2[:16], 2)
        time.sleep(0.02)

    def scroll(self, line, text, delay_ms, stop_event):
        if line not in (1, 2):
            return

        width = 16
        padding = " " * width
        text = padding + text + padding
        i = 0

        while not stop_event.is_set():
            window = text[i:i+width]
            self.lcd.lcd.display_string(window, line)
            time.sleep(delay_ms / 1000)
            i = (i + 1) % (len(text) - width)