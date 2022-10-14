from matrix import Matrix
from text_display import TextDisplay
from backdrop import StarBackdrop
from open_ble import BluetoothReceiver
import math, time, json

WIDTH = 64
HEIGHT = 32	
matrix = Matrix(width=WIDTH, height=HEIGHT, rotation=180)

# COLOR THEMES
# (base_)


#THEMES = {}
SHADOW = '0xFFFFFF'
BASIC = ('0xFF0000', '0xFFFFFF')
HALLOWEEN = ('0xFF7400', '0x6D0063')
CHRISTMAS = ('0x623004', '0x0B601C')


# BOOLS
isSparkling = True
isSignOn = True

# VARS
theme = BASIC
ftime = 0

################################
#
# OPEN SIGN
#

def openInit():
    global td, theme, isSparkling

    #load state from file
    '''
    with open('state.txt', 'r') as state:
        temp_dict = json.loads(state.read().rstrip())
        #temp_keys = temp_dict.keys()

        theme = tuple(temp_dict["theme"])
        print(theme)
        isSparkling = temp_dict["isSparkling"]
    '''
    
    font = 'fonts/IBMPlexMono-Bold-29.bdf'
    td = TextDisplay(matrix, font, theme[0])
    #td2 = TextDisplay(matrix, font2, '0xFF0000')
    td.loadText('OPEN', spacing=2)

    td.drawText('OPEN', posx=1, posy=1, spacing=2, font_color=theme[1])
    td.drawText('OPEN', posx=0, posy=0, spacing=2 )

def openUpdate():
    td.dynamicChar('OPEN', posx=0, posy=0, spacing=2, charDelay=350, aniDelay=2500, color1=theme[0], color2=theme[1])


def sparklingInit():
    global stars

    stars = StarBackdrop(matrix, delay=50, num_stars=25)

def sparklingUpdate():
    stars.updateStars()

def btInit():
    global btr

    btr = BluetoothReceiver()
    btr.allowConnection()

def btUpdate():
    if btr.ble.connected:

        btr.checkConnection() #this may be redundant
        while btr.isConnected:
            btr.listen()
            if btr.hasCommand:
                print(btr.command)
                #do something with command

                executeCommand()

                btr.command = ""
                btr.hasCommand = False
            btr.checkConnection()

        #Allow for reconnection after disconnect
        btr.allowConnection()

def executeCommand():
    global theme, isSparkling, isSignOn

    c = btr.command.upper()

    if c == "BA":
        theme = BASIC
    elif c == "HW":
        theme = HALLOWEEN
    elif c == "XS":
        theme = CHRISTMAS
    elif c == "S":
        isSparkling = True
    elif c == "NS":
        isSparkling = False
    elif c == "OFF":
        isSignOn = False
    elif c == "ON":
        isSignOn = True 
    
    matrix.clear()
    if isSignOn:
        openInit()
        openUpdate()

    matrix.flip()

    #notify user of successful command
    btr.ackCommand(c)
    
    '''
    #write new state to file
    #HAD TO CHANGE TO READ, CUZ READ-ONLY OS
    with open('state.txt', 'r') as state:
        temp_dict = {}
        temp_dict["theme"] = theme
        temp_dict["isSparkling"] = isSparkling

        #state.write(json.dumps(temp_dict))
    '''
    
###############
## MAIN CODE ##
###############

btInit()
openInit()
sparklingInit()

while True:
    btUpdate()

    if isSignOn:
        openUpdate()
        if isSparkling:
            sparklingUpdate()

        matrix.flip()