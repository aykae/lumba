from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
import terminalio
from adafruit_airlift.esp32 import ESP32

from adafruit_display_text import label
from adafruit_matrixportal.matrix import Matrix

#BLE Setup
esp32 = ESP32()

adapter = esp32.start_bluetooth()

ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)

#Matrix Setup
matrix = Matrix(width=64, height=32, rotation=180)
display = matrix.display
text = "LUMBA"
tb = label.Label(terminalio.FONT, text=text, background_color=0x800000)
tb.y = 10
tb.scale = 2
display.show(tb)

def echo():
    ble.start_advertising(advertisement)
    print("waiting to connect")
    while not ble.connected:
        pass
    print("connected: trying to read input")
    while ble.connected:
        # Returns b'' if nothing was read.
        one_byte = uart.read(1)
        if one_byte:
            print(one_byte)
            uart.write(one_byte)

def sendWord():
    ble.start_advertising(advertisement)
    print("waiting to connect")
    while not ble.connected:
        pass
    print("connected: trying to read input")
    while ble.connected:
        # Returns b'' if nothing was read.
        data = uart.read(1)
        if data:
            uart.write(data)

def displayWord():
    ble.start_advertising(advertisement)
    print("Waiting to connect...")
    while not ble.connected:
        pass
    print("Connected: attempting to read input")
    while ble.connected:
        msg = ""
        data = uart.read(1).decode()
        while data != '\n':
            msg += data
            data = uart.read(1).decode()

        print(msg)
        tb.text = msg
        display.show(tb)


while True:
    displayWord()