from adafruit_bitmap_font import bitmap_font


class TextDisplay():
    def __init__(
        self,
        matrix,
        font_file,
    ):
        self.matrix = matrix
        self.font = bitmap_font.load_font(font_file)

    def displayStatic(self, msg):
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


