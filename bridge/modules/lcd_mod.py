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

        # Internal state of both lines (for single-argument display_string)
        self.line1 = ""
        self.line2 = ""

    # ---------- Internal helpers ----------

    def _render(self):
        """
        Send current buffer (line1 + line2) to the LCD.
        Uses a single display_string call compatible with the HD44780MCP API
        that accepts only one positional argument.
        """
        text = f"{self.line1[:self.lcd_cols]}\n{self.line2[:self.lcd_cols]}"
        self.lcd.display_string(text)
        time.sleep(0.02)

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
        self.line1 = ""
        self.line2 = ""
        self.lcd.clear_display()
        time.sleep(0.02)

    # ---------- Writing helpers ----------

    def write(self, text):
        self.on()
        self.line1 = text[:self.lcd_cols]
        self.line2 = ""
        self.lcd.clear_display()
        self._render()

    def write_line(self, line, text):
        if line not in (1, 2):
            return
        self.on()
        if line == 1:
            self.line1 = text[:self.lcd_cols]
        else:
            self.line2 = text[:self.lcd_cols]
        self._render()

    def write_both(self, line1, line2):
        self.on()
        self.line1 = line1[:self.lcd_cols]
        self.line2 = line2[:self.lcd_cols]
        self.lcd.clear_display()
        self._render()

    # ---------- Horizontal scroll ----------

    def scroll(self, line, text, delay_ms, stop_event):
        if line not in (1, 2):
            return

        self.on()

        # Clamp speed to at least 1 ms to avoid zero/negative sleeps
        if delay_ms < 1:
            delay_ms = 1

        # Start from a clean screen for more predictable behaviour
        self.clear()

        width = self.lcd_cols
        padding = " " * width
        display_text = padding + text + padding

        i = 0
        while not stop_event.is_set():
            window = display_text[i:i + width]

            if line == 1:
                self.line1 = window
                self.line2 = ""
            else:
                self.line1 = ""
                self.line2 = window

            self._render()
            time.sleep(delay_ms / 1000.0)

            i += 1
            if i > len(display_text) - width:
                i = 0
