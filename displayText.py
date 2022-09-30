import displayio
from adafruit_matrixportal.matrix import Matrix

matrix = Matrix(width=64, height=32)
display = matrix.display

bitmap = displayio.Bitmap(display.width, display.height, 1)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
group.append(tile_grid)

display.show(group)

for i in range(display.width):
    bitmap[i, 0] = 1

while True:
    pass