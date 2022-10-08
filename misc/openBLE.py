# A BLE Script for the peripheral, Lumba's customizable Open Sign 
# Created by AK, Lumba Technologies

from adafruit_ble import BLERadio
from adafriut_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_airlift.esp32 import ESP32

esp32 = ESP32()
adapter = esp32.start_bluetooth()

ble = BLERadio(adapter)
uart = UARTService()
advert = ProvideServicesAdvertisement(uart)

while True:
    ble.stop_advertising(advert)
    ble.start_advertising(advert)
    print("Attempting to connect...")

    while not ble.connected:
        pass
    print("Connection Successful. Waiting for instruction...")

    while ble.connected:
        txt = ""
        byte = uart.read(1).decode()
        while byte != "\n":
            txt += byte
            byte = uart.read(1).decode()

        print(txt)
        #use txt to update screen
        ### ->




