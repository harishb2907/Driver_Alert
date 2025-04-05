import RPi.GPIO as GPIO
import smbus2  # I2C Communication Library
import time
import os  # For running system commands

# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin connected to MQ-3 digital output
ALCOHOL_SENSOR_PIN = 17
GPIO.setup(ALCOHOL_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use Pull-Down Resistor

# I2C LCD Setup
I2C_ADDR = 0x27  # Change to 0x3F if needed
bus = smbus2.SMBus(1)

# LCD Commands
LCD_WIDTH = 16
LCD_CHR = 1
LCD_CMD = 0

LCD_LINE_1 = 0x80  # 1st Line
LCD_LINE_2 = 0xC0  # 2nd Line

ENABLE = 0b00000100  # Enable bit
BACKLIGHT = 0b00001000  # Backlight On

def lcd_byte(bits, mode):
    """ Send byte data to I2C LCD """
    high_bits = mode | (bits & 0xF0) | BACKLIGHT
    low_bits = mode | ((bits << 4) & 0xF0) | BACKLIGHT
    bus.write_byte(I2C_ADDR, high_bits)
    lcd_toggle_enable(high_bits)
    bus.write_byte(I2C_ADDR, low_bits)
    lcd_toggle_enable(low_bits)

def lcd_toggle_enable(bits):
    """ Toggle enable pin for I2C LCD """
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits | ENABLE))
    time.sleep(0.0005)
    bus.write_byte(I2C_ADDR, (bits & ~ENABLE))
    time.sleep(0.0005)

def lcd_init():
    """ Initialize the I2C LCD Display """
    lcd_byte(0x33, LCD_CMD)
    lcd_byte(0x32, LCD_CMD)
    lcd_byte(0x06, LCD_CMD)
    lcd_byte(0x0C, LCD_CMD)
    lcd_byte(0x28, LCD_CMD)
    lcd_byte(0x01, LCD_CMD)
    time.sleep(0.005)

def lcd_string(message, line):
    """ Display message on LCD screen """
    message = message.ljust(LCD_WIDTH, " ")
    lcd_byte(line, LCD_CMD)
    for char in message:
        lcd_byte(ord(char), LCD_CHR)

def speak_alert():
    """ Function to generate an audio alert using text-to-speech (TTS) """
    os.system('espeak "Warning! Alcohol detected!"')

# Initialize LCD
lcd_init()
lcd_string("Alcohol Detector", LCD_LINE_1)
lcd_string("Initializing...", LCD_LINE_2)
time.sleep(2)

print("Alcohol detection system started...")

# Infinite loop
while True:
    alcohol_detected = GPIO.input(ALCOHOL_SENSOR_PIN)  # Read sensor

    if alcohol_detected == 1:  # Change to 0 if sensor works oppositely
        print("ALCOHOL DETECTED! Triggering alert...")
        lcd_string("ALCOHOL ALERT!", LCD_LINE_1)
        lcd_string("Take Action!", LCD_LINE_2)
        speak_alert()
    else:
        print("No alcohol detected.")
        lcd_string("No Alcohol", LCD_LINE_1)
        lcd_string("All Clear", LCD_LINE_2)

    time.sleep(2)  # Delay to avoid rapid alerts
