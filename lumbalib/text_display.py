from adafruit_bitmap_font import bitmap_font


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
        self.matrix.display.refresh()

    def drawText(self, txt, spacing=1):
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(txt)

        dx = 0
        for i in txt:
            glyph = self.font.get_glyph(ord(i))
            for y in range(glyph.bitmap.height):
                for x in range(glyph.bitmap.width):
                    val = glyph.bitmap[x,y]
                    if val > 0:
                        self.matrix.setPixel(dx + x, y, self.font_color)
            dx += glyph.bitmap.width
            dx += spacing

        self.matrix.display.refresh()

