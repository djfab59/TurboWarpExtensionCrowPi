from Adafruit_LED_Backpack import SevenSegment
import time

segment = SevenSegment.SevenSegment(address=0x70)
segment.begin()
segment.clear()
segment.write_display()

print("Test des chiffres (set_digit)")
for pos in range(4):
    segment.clear()
    segment.set_digit(pos, 8)  # all segments ON pour ce digit
    segment.write_display()
    input(f"-> Regarde quel chiffre s'allume pour set_digit({pos}, 8), puis Entrée...")

print("\nTest des points décimaux (set_decimal)")
for pos in range(4):
    segment.clear()
    segment.set_digit(0, 0)
    segment.set_digit(1, 0)
    segment.set_digit(2, 0)
    segment.set_digit(3, 0)
    segment.set_decimal(pos, True)
    segment.write_display()
    input(f"-> Regarde quel point s'allume pour set_decimal({pos}, True), puis Entrée...")

print("\nTest du deux-points (set_colon)")
segment.clear()
segment.set_colon(True)
segment.write_display()
input("-> Regarde où s'allume le ':', puis Entrée...")

segment.clear()
segment.write_display()
print("Test terminé.")
