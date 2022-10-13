from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_airlift.esp32 import ESP32

class BluetoothReceiver:

    command = ""
    isConnected = False
    hasCommand = False

    def __init__(self):
        esp32 = ESP32()
        adapter = esp32.start_bluetooth()

        self.ble = BLERadio(adapter)
        self.uart = UARTService()
        self.advert = ProvideServicesAdvertisement(self.uart)


    def allowConnection(self):
        try:
            self.ble.stop_advertising()
        except:
            pass

        self.ble.start_advertising(self.advert)


    def checkConnection(self):
        if not self.isConnected:
            if self.ble.connected:
                self.isConnected = True
                print("Connection Successful. Waiting for command...")
        else:
            if not self.ble.connected:
                self.isConnected = False
                print("Connection Lost. Come back soon.")


    def listen(self):
        byte = self.uart.read(1).decode()
        if not self.hasCommand and byte != "\n":
            self.command += byte
        else:
            self.hasCommand = True

    #acknowledge that command was executed.        
    def ackCommand(self, command):
        msg = ""
        if c == "BA":
            msg = "Color scheme switched to Basic."
        elif c == "HW":
            msg = "Color scheme switched to Halloween."
        elif c == "XS":
            msg = "Color scheme switched to Christmas."
        elif c == "S":
            msg = "Sparkling animation was enabled."
        elif c == "NS":
            msg = "Sparkling animation was disabled."
        elif c == "OFF":
            msg = "Sign was switched off."
        elif c == "ON":
            msg = "Sign was switched on."
        
        self.uart.write(msg)







