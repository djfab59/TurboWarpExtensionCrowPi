#!/usr/bin/env python3

import HD44780MCP
import MCP230XX

class LCDModule:
    def __init__(self):
        self.address = 0x21
        self.lcd_cols = 16
        self.lcd_rows = 2
        self.bl_pin = 7

        self.mcp = MCP230XX.MCP230XX('MCP23008', self.address)
        self.lcd = HD44780MCP.HD44780(
            self.mcp,
            1, -1, 2,
            dbList=[3, 4, 5, 6],
            rows=self.lcd_rows,
            characters=self.lcd_cols
        )
        self.mcp.set_mode(self.bl_pin, 'output')

    def on(self):
        self.mcp.output(self.bl_pin, 1)
        self.lcd.set_display(on=1, cursor=0)

    def off(self):
        self.lcd.clear_display()
        self.mcp.output(self.bl_pin, 0)

    def clear(self):
        self.lcd.clear_display()

    def write(self, text):
        self.on()
        self.lcd.clear_display()
        self.lcd.display_string(text[:16])

