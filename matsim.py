import pygame

pygame.init()

display = pygame.display

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500

MATRIX_WIDTH = 64
MATRIX_HEIGHT = 32
PIXEL_SIZE = 10 
PIXEL_SPACING = 5 

def initMatrix():
    dx = 0
    dy = 0
    px = 0
    py = 0
    for y in range(WINDOW_HEIGHT):
        for x in range(WINDOW_WIDTH):
            if px < MATRIX_WIDTH and dx <= x < (dx + PIXEL_SIZE):
                if py < MATRIX_HEIGHT and dy <= y < (dy + PIXEL_SIZE):
                    window.set_at((x,y), (0, 0, 0))
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
    print("iT RAN")
###
#MAIN LOOP
###

window = display.set_mode((1000, 500))
running = True
window.fill((150, 150, 150))

initMatrix()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
exit()