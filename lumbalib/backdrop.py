import random, time

class StarBackdrop():
    def __init__(self, matrix):
        self.matrix = matrix
        self.autoplay = True

        self.stardict = {}

        self.maxstars = 10
        self.color = 10
        self.brightness = 255

        self.lastTime

    def rgbToHex(self, r, g, b):
        return "0x%02x%02x%02x" % (r, g, b)

    def updateStars(self):
        for i in maxstars:
            sx = random.randint(0, self.matrix.width)
            sy = random.randint(0, self.matrix.height)

            if self.matrix.getPixel(sx, sy) > 0:
                self.stardict[(sx, sy)] = rgbToHex(255, 255, 255)


        #DONT OVERWRITE TEXT PIXELS
        return

    
    
