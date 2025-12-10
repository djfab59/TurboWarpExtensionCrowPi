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

    # ---------- LCD basics ----------

    def on(self):
        self.mcp.output(self.bl_pin, 1)
        # Désactive le curseur pour éviter l'underscore final
        self.lcd.set_display(on=1, cursor=0)
        time.sleep(0.02)

    def off(self):
        self.lcd.clear_display()
        self.mcp.output(self.bl_pin, 0)
        time.sleep(0.02)

    def clear(self):
        self.lcd.clear_display()
        time.sleep(0.02)

    # ---------- Writing helpers ----------

    def write(self, text):
        self.on()
        self.lcd.clear_display()
        self.lcd.display_string(text[:16])
        time.sleep(0.02)

    def write_line(self, line, text):
        if line not in (1, 2):
            return
        self.on()
        text = text[:16]
        self.lcd.display_string(text, line)
        time.sleep(0.02)

    def write_both(self, line1, line2):
        self.on()
        self.lcd.clear_display()
        time.sleep(0.02)
        self.lcd.display_string(line1[:16], 1)
        self.lcd.display_string(line2[:16], 2)
        time.sleep(0.02)

    # ---------- Horizontal scroll ----------

    def scroll(self, line, text, delay_ms, stop_event):
        if line not in (1, 2):
            return

        self.on()

        width = 16
        padding = " " * width
        display_text = padding + text + padding

        i = 0
        while not stop_event.is_set():
            window = display_text[i:i + width]
            self.lcd.display_string(window, line)
            time.sleep(delay_ms / 1000.0)

            i += 1
            if i > len(display_text) - width:
                i = 0
