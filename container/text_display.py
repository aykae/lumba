from adafruit_bitmap_font import bitmap_font
import math
import time

class TextDisplay():
    def __init__(
        self,
        matrix,
        font_file,
        font_color,
    ):
        self.matrix = matrix
        self.font = bitmap_font.load_font(font_file)
        self.font_color = font_color

    def drawLetter(self, l):
        #only height and dy are relevant, because we want the width and dx to vary with character size
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(l)

        glyph = self.font.get_glyph(ord(l))
        for y in range(glyph.bitmap.height):
            for x in range(glyph.bitmap.width):
                val = glyph.bitmap[x, y]
                if val > 0:
                    self.matrix.setPixel(x, y, self.font_color)
                    #ALT: FILL DICTIONARY WITH PIXELS TO DRAW,
                        # WON'T SPEED UP THIS FUNCTION, BUT FOR FUTURE
                        # CACHING
        self.flip()

    def drawText(self, txt, spacing=1, centered=True, posx=0, posy=0, font_color=None):
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(txt)

        if not font_color:
            font_color = self.font_color

        #DEFAULT CENTERING FEATURE
        txtWidth = 0
        txtHeight = 0
        for i in txt:
            glyph = self.font.get_glyph(ord(i))
            txtWidth += glyph.bitmap.width + spacing
            txtHeight = glyph.bitmap.height
        txtWidth -= spacing

        if centered:
            cx = (self.matrix.display.width // 2 - 1) - txtWidth // 2 
            cy = (self.matrix.display.height // 2 - 1) - txtHeight // 2

        dx = 0
        for i in txt:
            glyph = self.font.get_glyph(ord(i))
            for y in range(glyph.bitmap.height):
                for x in range(glyph.bitmap.width):
                    val = glyph.bitmap[x,y]
                    if val > 0:
                        self.matrix.setPixel(cx + posx + dx + x, cy + posy + y, font_color)
            dx += glyph.bitmap.width
            dx += spacing

    def floatingText(self, txt, speed=1, amplitude=10, spacing=1):
        
        self.drawText(txt, posx=0, posy=dy)
        dy += speed