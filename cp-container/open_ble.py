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
        c = command[0].upper()

        msg = ""
        if c == "?" or c == "HELP" or c == "MENU":
            msg = "Here are your available commands: \n"
            msg += "\t Change Color Scheme:\n"
            msg += "\t\t BA -> Basic, White and Red\n"
            msg += "\t\t HW -> Halloween, Orange and Purple\n"
            msg += "\t\t XS -> Christmas, Red and Green\n"
            msg += "\n"

            msg += "\t Set Animation:\n"
            msg += "\t\t S: Enable sparkles\n"
            msg += "\t\t NS: Disable sparkles\n"
            msg += "\t\t H: Enable letter highlight\n"
            msg += "\t\t NH: Disable letter highlight\n"
            msg += "\n"

            msg += "\t Change Text:\n"
            msg += "\t\t TEXT {your word}\n"
            msg += "\n"

            msg += "\t Power:\n"
            msg += "\t\t OFF: Turn Sign Off\n"
            msg += "\t\t ON: Turn Sign On\n"

        elif c == "BA":
            msg = "Color scheme switched to Basic."
        elif c == "HW":
            msg = "Color scheme switched to Halloween."
        elif c == "XS":
            msg = "Color scheme switched to Christmas."
        elif c == "S":
            msg = "Sparkling animation was enabled."
        elif c == "NS":
            msg = "Sparkling animation was disabled."
        elif c == "H":
            msg = "Letter highlight was enabled."
        elif c == "NH":
            msg = "Letter highlight was disabled."
        elif c == "TEXT":
            if len(command) > 1:
                t = command[1]
                if len(t) <= 4:
                    msg = "Text was changed to \"" + t + "\"."
                else:
                    msg = "Unsuccessful. Text must be four characters or less."
            else:
                msg = "Unsuccessful. Text must typed after the \"TEXT\" command."
        elif c == "OFF":
            msg = "Sign was switched off."
        elif c == "ON":
            msg = "Sign was switched on."
        else:
            msg = "Command does not exist. Type \"?\" to see available commands."

        msg += "\n" 
        self.uart.write(msg)







