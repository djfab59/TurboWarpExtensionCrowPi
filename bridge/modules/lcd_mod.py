import time
import MCP230XX
import HD44780MCP

class LCD:
    def __init__(self):
        # I2C / LCD configuration
        self.address = 0x21
        self.lcd_cols = 16
        self.lcd_rows = 2
        self.bl_pin = 7

        # MCP23008
        self.mcp = MCP230XX.MCP230XX('MCP23008', self.address)

        # HD44780 via MCP
        self.lcd = HD44780MCP.HD44780(
            self.mcp,
            1, -1, 2,
            dbList=[3, 4, 5, 6],
            rows=self.lcd_rows,
            characters=self.lcd_cols
        )

        # Backlight
        self.mcp.set_mode(self.bl_pin, 'output')
        self.on()

    # ---------- LCD basics ----------

    def on(self):
        self.mcp.output(self.bl_pin, 1)

    def off(self):
        self.mcp.output(self.bl_pin, 0)

    def clear(self):
        self.lcd.clear_display()
        time.sleep(0.02)

    # ---------- Writing helpers ----------

    def write(self, text):
        self.clear()
        self.lcd.display_string(text[:16])
        time.sleep(0.02)

    def write_line(self, line, text):
        if line not in (1, 2):
            return
        self.lcd.display_string(text[:16])
        time.sleep(0.02)

    def write_both(self, line1, line2):
        self.clear()
        # La bibliothèque HD44780MCP semble accepter une seule chaîne
        # (avec éventuellement un retour à la ligne pour la 2e ligne).
        self.lcd.display_string(f"{line1[:16]}\n{line2[:16]}")
        time.sleep(0.02)

    # ---------- Horizontal scroll ----------

    def scroll(self, line, text, delay_ms, stop_event):
        if line not in (1, 2):
            return

        width = self.lcd_cols
        padding = " " * width
        text = padding + text + padding
        index = 0

        while not stop_event.is_set():
            window = text[index:index + width]
            self.lcd.display_string(window)
            time.sleep(delay_ms / 1000)
            index = (index + 1) % (len(text) - width)
