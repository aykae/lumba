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
def sparklingInit():
    global stars, font, td

    font = 'fonts/IBMPlexMono-Medium-24.bdf'
    td = TextDisplay(matrix, font, '0xFF0000')

    td.drawText('OPEN', posx=0, posy=0, font_color='0xFFFFFF')
    td.drawText('OPEN', posx=1, posy=1)

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
    font = 'fonts/IBMPlexMono-Medium-24.bdf'
    td = TextDisplay(matrix, font, '0xFF0000')


def floatingUpdate():
    global ftime

    dy = int(8 * math.sin(ftime))
    td.drawText(text, posy=dy)

    ftime += 0.5


#sparklingInit()
floatingInit()
while True:
    #sparklingUpdate()
    floatingUpdate()
    matrix.flip()
    matrix.clear()