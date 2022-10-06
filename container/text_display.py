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

        self.currChar = 0
        self.ddx = 0 #dynamic dx
        self.prevDdx = -1 #dynamic dx
        self.lastTimeChar = time.monotonic() #last time character was drawn
        self.lastTimeAni = time.monotonic() #last time animation started
        self.playingAni = False #currently playing animation

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

    #Dynamic Sequence of Text
    def dynamicSeqDrawText(self, txt, delay=500, spacing=1, centered=True, posx=0, posy=0, font_color=None):
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


        if time.monotonic() > self.lastTime + (delay / 1000.0):
            glyph = self.font.get_glyph(ord(txt[self.currChar]))
            for y in range(glyph.bitmap.height):
                for x in range(glyph.bitmap.width):
                    val = glyph.bitmap[x,y]
                    if val > 0:
                        self.matrix.setPixel(cx + posx + self.ddx + x, cy + posy + y, font_color)
            self.ddx += glyph.bitmap.width
            self.ddx += spacing

            self.last_time = time.monotonic()
            self.curr_char = (self.currChar + 1) % len(txt)
            if self.curr_char == 0:
                self.ddx = 0

    #Dynamic characters of Text
    def dynamicCharDrawText(self, txt, color1, color2, charDelay=500, aniDelay=1000, spacing=1, centered=True, posx=0, posy=0):
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


        if time.monotonic() > self.lastTimeAni + (aniDelay / 1000.0):

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
                    self.lastTimeAni = time.monotonic()
                    self.playingAni = False

                    #animation concluded, unhighlight previous character
                    prevChar = (self.currChar - 1) % len(txt)
                    if self.prevDdx >= 0:
                        glyph = self.font.get_glyph(ord(txt[prevChar]))
                        for y in range(glyph.bitmap.height):
                            for x in range(glyph.bitmap.width):
                                val = glyph.bitmap[x,y]
                                if val > 0:
                                    self.matrix.setPixel(cx + posx + self.prevDdx + x, cy + posy + y, color1)
                    
    #Dynamic characters of Text
    def dynamicCharLoopDrawText(self, txt, color1, color2, charDelay=500, spacing=1, centered=True, posx=0, posy=0):
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