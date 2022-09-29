import board
from adafruit_matrixportal.matrixportal import MatrixPortal

WIDTH = 64
HEIGHT = 32
FONT = "/IBMPlexMono-Medium-24_jep.bdf"

mp = MatrixPortal(width=WIDTH, height=HEIGHT)

mp.add_text(
    text_font = FONT,
    text_position = (
        0,0
        #(mp.graphics.display.width)
    ),
    text_color=0x800000
)

mp.set_text("LUMBA")

while True:
    continue
    #time.sleep()