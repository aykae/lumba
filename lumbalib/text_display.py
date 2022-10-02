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
            if not glyph:
                continue
            for x in range(glyph.bitmap.width):
                val = glyph.bitmap[x, y]
                if val > 0:
                    self.matrix.setPixel(x, y, self.font_color)
                    #ALT: FILL DICTIONARY WITH PIXELS TO DRAW,
                        # WON'T SPEED UP THIS FUNCTION, BUT FOR FUTURE
                        # CACHING
        self.matrix.display.refresh()

    def drawLetterBroke(self, l):
        #only height and dy are relevant, because we want the width and dx to vary with character size
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(l)
        print(height)
        print(dy)
        for y in range(height):
            glyph = self.font.get_glyph(ord(l))
            print(glyph.dy)
            print(glyph.height)
            print(glyph.dx)
            print(glyph.shift_x)
            if not glyph:
                continue
            glyph_y = y + glyph.dy
            for x in range(glyph.shift_x):
                glyph_x = x + glyph.dx
                val = glyph.bitmap[glyph_x, glyph_y]
                if val > 0:
                    self.matrix.setPixel(x, y, self.font_color)
                    #ALT: FILL DICTIONARY WITH PIXELS TO DRAW,
                        # WON'T SPEED UP THIS FUNCTION, BUT FOR FUTURE
                        # CACHING
        self.matrix.display.refresh()


    def drawStatic(self, msg):
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(msg)

        for y in range(height):
            for c in msg:
                glyph = self.font.get_glyph(ord(c))
                if not glyph:
                    continue

                glyph_y = y + (glyph.height - (height + dy) + glyph.dy)
                pixels = []
                if 0 <= glyph_y < glyph.height:
                    for i in range(glyph.width):
                        value = glyph.bitmap[i, glyph_y]
                        pixel = ' ' #PRINT NOTHING, BLACK FOR MATRIX
                        if value > 0:
                            pixel = '#' #PRINT SOMETHING, FONT COLOR FOR MATRIX
                else:
                    pixels = ''
                print(''.join(pixels) + ' ' * (glyph.shift_x - len(pixels)), end='')
            print()


