#from lumba_matrix.matrix import Matrix
from matrix import Matrix

WIDTH = 64
HEIGHT = 32
matrix = Matrix(width=WIDTH, height=HEIGHT)


matrix.setPixel(WIDTH-1, HEIGHT-1, 0, 255, 0)

while True:
    matrix.display.refresh()