from lumba_matrix.matrix import Matrix

matrix = Matrix(width=64, height=32)

try:
    matrix.setPixel(0, 0, 0, 0, 0)
except:
    print("caught exception")

while True:
    pass