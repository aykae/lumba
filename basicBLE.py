import board
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_airlift.esp32 import ESP32
from adafruit_matrixportal.matrixportal import MatrixPortal

#MATRIX Setup

WIDTH = 64
HEIGHT = 32
FONT = "/IBMPlexMono-Medium-24_jep.bdf"

mp = MatrixPortal(width=WIDTH, height=HEIGHT)

#BLE Setup
esp32 = ESP32()

adapter = esp32.start_bluetooth()

ble = BLERadio(adapter)
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)


#prepare text
mp.add_text(
    text_font = FONT,
    text_position = (
        0,0
        #(mp.graphics.display.width)
    ),
    text_color=0x800000
)

mp.set_text("LUMBA")

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
            mp.set_text(str(data))

while True:
    echo()