import pygame


MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
PIXEL_SIZE = 12
PIXEL_SPACING = 2

X_OFFSET = 20
Y_OFFSET = 20

WINDOW_WIDTH = (MATRIX_WIDTH * (PIXEL_SIZE + PIXEL_SPACING)) + 2 * (X_OFFSET)
WINDOW_HEIGHT = (MATRIX_HEIGHT * (PIXEL_SIZE + PIXEL_SPACING)) + 2 * (Y_OFFSET)

BG_GRAY = 25
BG_COLOR = (BG_GRAY, BG_GRAY, BG_GRAY)

def initMatrix():
    dx = 0
    dy = 0
    px = 0
    py = 0
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            if px < MATRIX_WIDTH and dx <= x < (dx + PIXEL_SIZE):
                if py < MATRIX_HEIGHT and dy <= y < (dy + PIXEL_SIZE):
                    window.set_at((x + X_OFFSET, y + Y_OFFSET), ("0x000000"))
            else:
                #increment x pixel
                if x - dx == (PIXEL_SIZE + PIXEL_SPACING - 1) and px < MATRIX_WIDTH:
                    px += 1
                    dx += (PIXEL_SIZE + PIXEL_SPACING)

        #increment y pixel
        if y - dy == (PIXEL_SIZE + PIXEL_SPACING - 1) and py < MATRIX_HEIGHT:
            py += 1
            dy += (PIXEL_SIZE + PIXEL_SPACING)

        #reset x vars for next row
        dx = 0
        px = 0

    display.flip()

def setPixel(x, y, hexcolor):
    dx = x * (PIXEL_SIZE + PIXEL_SPACING) + X_OFFSET
    dy = y * (PIXEL_SIZE + PIXEL_SPACING) + Y_OFFSET

    for y in range(PIXEL_SIZE):
        for x in range(PIXEL_SIZE):
            window.set_at((dx + x, dy + y), (hexcolor))

###
#MAIN LOOP
###

pygame.init()
display = pygame.display

window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
window.fill(BG_COLOR)

initMatrix()

###
#MAIN CODE
###
setPixel(5, 5, "0xFF0000")
display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
exit()