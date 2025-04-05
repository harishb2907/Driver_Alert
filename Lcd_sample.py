import smbus2
import time

I2C_ADDR = 0x27  # Change to 0x3F if needed
bus = smbus2.SMBus(1)  # Use SMBus(0) if i2c-1 doesn't exist

LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80  # 1st Line
LCD_LINE_2 = 0xC0  # 2nd Line
ENABLE = 0b00000100
BACKLIGHT = 0b00001000

def lcd_byte(bits, mode):
    """ Send byte data to LCD """
    high_bits = mode | (bits & 0xF0) | BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | BACKLIGHT
    bus.write_byte(I2C_ADDR, high_bits)
    lcd_toggle_enable(high_bits)
    bus.write_byte(I2C_ADDR, low_bits)
    lcd_toggle_enable(low_bits)

def lcd_toggle_enable(bits):
    """ Toggle enable pin for LCD """
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(0.0005)

def lcd_init():
    """ Initialize LCD """
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.005)

def lcd_string(message, line):
    """ Display message on LCD """
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

# Initialize LCD and display test message
lcd_init()
lcd_string("Hello, Raspberry!", LCD_LINE_1)
lcd_string("LCD is working!", LCD_LINE_2)
