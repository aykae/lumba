import random, time
import colorcon

class StarBackdrop():
    def __init__(self, matrix, delay=100, num_stars=10):
        self.matrix = matrix
        self.autoplay = True

        self.stardict = {}

        self.maxStars = num_stars
        self.color = 10
        self.brightness = 255

        self.lastTime = time.monotonic()
        self.delay = delay

    def checkForAdjacent(self, star):
        keys = self.stardict.keys()
        if (star[0] + 1, star[1]) in keys:
            return True
        elif (star[0] - 1, star[1]) in keys:
            return True
        elif (star[0], star[1] + 1) in keys:
            return True
        elif (star[0] + 1, star[1] - 1) in keys:
            return True

        return False

    def updateStars(self):
        #OPT: calculate next stars in delay gaps

        if time.monotonic() > self.lastTime + (self.delay / 1000.0):
            for i in self.stardict.keys():
                self.matrix.setPixel(i[0], i[1], "0x000000")
                self.stardict.pop(i)

            for i in range(self.maxStars):
                sx = random.randint(0, self.matrix.display.width)
                sy = random.randint(0, self.matrix.display.height)

                #hasAdjacent = self.checkForAdjacent((sx, sy))

                if self.matrix.getPixel(sx, sy) == 0: #and not hasAdjacent:
                    self.stardict[(sx, sy)] = colorcon.rgbToHex(255, 255, 255)

            for i in self.stardict.keys():
                self.matrix.setPixel(i[0], i[1], self.stardict[i])

            self.lastTime = time.monotonic()
