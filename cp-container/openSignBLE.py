from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_airlift.esp32 import ESP32

class BluetoothReceiver:

    command = ""

    def __init__(self):
        esp32 = ESP32()
        adapter = esp32.start_bluetooth()

        self.ble = BLERadio(adapter)
        self.uart = UARTService()
        self.advert = ProvideServicesAdvertisement(self.uart)


    def startListening(self):
        try:
            self.ble.stop_advertising()
        except:
            pass

        self.ble.start_advertising(self.advert)
        print("Attempting to connect...")

        while not self.ble.connected:
            pass
        print("Connection Successful. Waiting for command...")

        while self.ble.connected:
            self.command = ""
            byte = self.uart.read(1).decode()

            while byte != "\n" and self.ble.connected:
                self.command += byte
                byte = self.uart.read(1).decode()

            print(self.command)






