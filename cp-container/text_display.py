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

        self.buffer = {}

        self.currChar = 0

        self.lastTime = time.monotonic()
        self.lastTimeChar = time.monotonic() #last time character was drawn
        self.lastTimeAni = time.monotonic() #last time animation started

        self.aniStarted = False #animation started
        self.aniFinished = False #animation finished

    def loadText(self, txt, spacing=2):
        # Adds text to buffer with following specs
        # dict( text -> 
        #    dict( char -> list of pixel tuples,
        #         "center" -> (cx, cy)
        #        )
        # )

        if txt not in self.buffer.keys():
            txtWidth = 0
            txtHeight = 0

            empty_dict = {}
            self.buffer[txt] = empty_dict
            
            dx = 0
            for i in txt:
                empty_list = []
                self.buffer[txt][i] = empty_list
                glyph = self.font.get_glyph(ord(i))
                for y in range(glyph.bitmap.height):
                    for x in range(glyph.bitmap.width):
                        val = glyph.bitmap[x,y]
                        if val > 0:
                            self.buffer[txt][i].append((dx + x, y))
                dx += glyph.bitmap.width
                dx += spacing

                #calculate cumulative width and height
                glyph = self.font.get_glyph(ord(i))
                txtWidth += glyph.bitmap.width + spacing
                txtHeight = max(txtHeight, glyph.bitmap.height) #get greatest hight

            #calculate center of text
            txtWidth -= spacing
            cx = (self.matrix.display.width // 2 - 1) - txtWidth // 2 
            cy = (self.matrix.display.height // 2 - 1) - txtHeight // 2

            #add center to buffer for later use
            self.buffer[txt]["center"] = (cx, cy)
        else:
            print(txt + " has already been loaded.")


    def drawLetter(self, l, posx=0, posy=0):
        #only height and dy are relevant, because we want the width and dx to vary with character size
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(l)

        glyph = self.font.get_glyph(ord(l))
        for y in range(glyph.bitmap.height):
            for x in range(glyph.bitmap.width):
                val = glyph.bitmap[x, y]
                if val > 0:
                    self.matrix.setPixel(posx + x, posy + y, self.font_color)
                    #ALT: FILL DICTIONARY WITH PIXELS TO DRAW,
                        # WON'T SPEED UP THIS FUNCTION, BUT FOR FUTURE
                        # CACHING
        self.flip()

    def drawText(self, txt, spacing=1, centered=True, posx=0, posy=0, font_color=None):
        self.font.load_glyphs(txt)

        if not font_color:
            font_color = self.font_color

        buff_txt = self.buffer[txt]
        if centered:
            (cx, cy) = buff_txt['center']
        else:
            (cx, cy) = (0, 0)

        for ch in txt:
            for p in buff_txt[ch]:
                self.matrix.setPixel(cx + posx + p[0], cy + posy + p[1], font_color)

    def floatingText(self, txt, speed=1, amplitude=10, spacing=1):
        
        self.drawText(txt, posx=0, posy=dy)
        dy += speed

    #Dynamic characters of text no delay in between
    #Remove once dynamicCharDrawText optimized, since aniDelay=0 yields same effect
    def dynamicCharLoop(self, txt, color1, color2, charDelay=500, spacing=1, centered=True, posx=0, posy=0):
        _, height, _, dy = self.font.get_bounding_box()
        self.font.load_glyphs(txt)

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


        if time.monotonic() > self.lastTimeChar + (charDelay / 1000.0):
            
            #Unhighlight previous character
            prevChar = (self.currChar - 1) % len(txt)
            if self.prevDdx >= 0:
                glyph = self.font.get_glyph(ord(txt[prevChar]))
                for y in range(glyph.bitmap.height):
                    for x in range(glyph.bitmap.width):
                        val = glyph.bitmap[x,y]
                        if val > 0:
                            self.matrix.setPixel(cx + posx + self.prevDdx + x, cy + posy + y, color1)

            #Highlight next character
            glyph = self.font.get_glyph(ord(txt[self.currChar]))
            for y in range(glyph.bitmap.height):
                for x in range(glyph.bitmap.width):
                    val = glyph.bitmap[x,y]
                    if val > 0:
                        self.matrix.setPixel(cx + posx + self.ddx + x, cy + posy + y, color2)
            self.prevDdx = self.ddx
            self.ddx += glyph.bitmap.width
            self.ddx += spacing

            self.lastTimeChar = time.monotonic()
            self.currChar = (self.currChar + 1) % len(txt)
            if self.currChar == 0:
                self.ddx = 0

    #Dynamic characters of Text
    def dynamicChar(self, txt, color1, color2, charDelay=500, aniDelay=3000, spacing=1, centered=True, posx=0, posy=0):
        
        buff_txt = self.buffer[txt]

        if centered:
            (cx, cy) = buff_txt['center']
        else:
            (cx, cy) = (0, 0)

        if time.monotonic() > self.lastTimeAni + (aniDelay / 1000.0):
            if time.monotonic() > self.lastTimeChar + (charDelay / 1000.0):
                
                #Unhighlight previous character
                prevChar = (self.currChar - 1) % len(txt)

                if self.aniStarted:
                    ch = txt[prevChar]
                    for p in buff_txt[ch]:
                        self.matrix.setPixel(cx + posx + p[0], cy + posy + p[1], color1)

                if not self.aniFinished:
                    self.aniStarted = True

                    ch = txt[self.currChar]
                    for p in buff_txt[ch]:
                        self.matrix.setPixel(cx + posx + p[0], cy + posy + p[1], color2)

                    self.lastTimeChar = time.monotonic()
                    self.currChar = (self.currChar + 1) % len(txt)
                    if self.currChar == 0:
                        self.aniFinished = True
                else:
                    #Animation finished
                    self.lastTimeAni = time.monotonic()
                    self.aniFinished = False
                    self.aniStarted = False
