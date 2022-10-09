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

############################
#
# OPEN SIGN
#

def openInit(theme=BASIC):
    global td1

    font1 = 'fonts/IBMPlexMono-Bold-29.bdf'
    td1 = TextDisplay(matrix, font1, theme[0])
    #td2 = TextDisplay(matrix, font2, '0xFF0000')

    td1.drawText('OPEN', posx=1, posy=1, spacing=2, font_color=SHADOW)
    td1.drawText('OPEN', posx=0, posy=0, spacing=2 )

def openUpdate(theme=BASIC):
    td1.dynamicCharDrawText('OPEN', posx=0, posy=0, spacing=2, charDelay=300, color1=theme[0], color2=theme[1])

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

###############
## MAIN CODE ##
###############

btr = BluetoothReceiver()

theme=BASIC
openInit(theme)
sparklingInit()
#floatingInit()

while True:

    #MATRIX BT UPDATE NEEDS TO BE EVERY LOOPA
    #only listen if connection is established
    #if br.hasCommand, execute it and set it to False

    sparklingUpdate()
    #floatingUpdate()
    openUpdate(theme)
    matrix.flip()