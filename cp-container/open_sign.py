from matrix import Matrix
from text_display import TextDisplay
from backdrop import StarBackdrop
from open_ble import BluetoothReceiver
import math, time

WIDTH = 64
HEIGHT = 32	
matrix = Matrix(width=WIDTH, height=HEIGHT, rotation=180)

# COLOR THEMES
# (base_)
SHADOW = '0xFFFFFF'
BASIC = ('0xFF0000', '0xFFFFFF')
HALLOWEEN = ('0xFF7400', '0x6D0063')
CHRISTMAS = ('0x623004', '0x0B601C')

# BOOLS
sparkleOn = True

# VARS
theme = BASIC

################################
#
# OPEN SIGN
#

def openInit(theme=BASIC):
    global td

    font = 'fonts/IBMPlexMono-Bold-29.bdf'
    td = TextDisplay(matrix, font, theme[0])
    #td2 = TextDisplay(matrix, font2, '0xFF0000')
    td.loadText('OPEN', spacing=2)

    td.drawText('OPEN', posx=1, posy=1, spacing=2, font_color=theme[1])
    td.drawText('OPEN', posx=0, posy=0, spacing=2 )

def openUpdate(theme=BASIC):
    td.dynamicChar('OPEN', posx=0, posy=0, spacing=2, charDelay=350, aniDelay=2000, color1=theme[0], color2=theme[1])


def sparklingInit():
    global stars, font, td

    stars = StarBackdrop(matrix, delay=50, num_stars=25)

def sparklingUpdate():
    stars.updateStars()

############################
#
# FLOATING OPEN
#

ftime = 0
def floatingInit():
    global td, text

    text = "OPEN"
    font = 'fonts/IBMPlexMono-Bold-75.bdf'
    td = TextDisplay(matrix, font, '0xFF0000')


def floatingUpdate():
    global ftime

    dy = int(8 * math.sin(ftime))
    td.drawText(text, posy=dy)

    ftime += 0.5

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
    global theme, sparkleOn

    c = btr.command.upper()

    if c == "BA":
        theme = BASIC
    elif c == "HW":
        theme = HALLOWEEN
    elif c == "XS":
        theme = CHRISTMAS
    elif c == "S":
        sparkleOn = True
    elif c == "NS":
        sparkleOn = False
    
    matrix.clear()
    openInit(theme)

###############
## MAIN CODE ##
###############

btInit()
theme=BASIC
openInit(theme)
sparklingInit()

while True:
    btUpdate()

    if sparkleOn:
        sparklingUpdate()
    openUpdate(theme)
    matrix.flip()