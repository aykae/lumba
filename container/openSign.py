from matrix import Matrix
from text_display import TextDisplay
from backdrop import StarBackdrop
import math, time

WIDTH = 64
HEIGHT = 32	
matrix = Matrix(width=WIDTH, height=HEIGHT, rotation=180)

############################
#
# SPARKLING OPEN
#

###############

def signBasicInit():
    global td1

    font1 = 'fonts/IBMPlexMono-Bold-29.bdf'
    td1 = TextDisplay(matrix, font1, '0xFF0000')
    #td2 = TextDisplay(matrix, font2, '0xFF0000')

    td1.drawText('OPEN', posx=1, posy=1, font_color='0xFFFFFF')
    td1.drawText('OPEN', posx=0, posy=0, )

def signBasicUpdate():
    td1.dynamicCharDrawText('OPEN', posx=0, posy=0, color1='0xFF0000', color2='0xFFFFFF')

###############

def signHalloweenInit():
    font1 = 'fonts/IBMPlexMono-Bold-29.bdf'
    orange = '0xFF7400'
    #orange = '0xF79D08'
    purple = '0x6D0063'
    td = TextDisplay(matrix, font1, orange)

    td.drawText('OPEN', posx=1, posy=1, font_color=purple)
    td.drawText('OPEN', posx=0, posy=0)

###############

def signThanksgivingInit():
    font1 = 'fonts/IBMPlexMono-Bold-29.bdf'
    yellow = '0xEBBA38'
    red = '0x623004'
    td = TextDisplay(matrix, font1, yellow)

    td.drawText('OPEN', posx=1, posy=1, font_color=red)
    td.drawText('OPEN', posx=0, posy=0)

def signChristmasInit():
    font1 = 'fonts/IBMPlexMono-Bold-29.bdf'
    red = '0x623004'
    green = '0x0B601C'
    td = TextDisplay(matrix, font1, red)

    td.drawText('OPEN', posx=1, posy=1, font_color=green)
    td.drawText('OPEN', posx=0, posy=0)


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


signBasicInit()
sparklingInit()
#floatingInit()
while True:
    sparklingUpdate()
    #floatingUpdate()
    signBasicUpdate()
    matrix.flip()