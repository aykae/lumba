import displayio
import terminalio
from adafruit_display_text import label
from adafruit_matrixportal.matrix import Matrix

matrix = Matrix(width=64, height=32)
display = matrix.display

bitmap = displayio.Bitmap(display.width, display.height, 1)

palette = displayio.Palette(2)
palette[0] = 0x000000
palette[1] = 0xffffff

for i in range(display.width):
    bitmap[i, 0] = 1

#Display bitmap using tile grids and groups

tile_grid = displayio.TileGrid(bitmap, pixel_shader=palette)
group = displayio.Group()
#group.append(tile_grid)

display.show(group)

#Display text using labels

text = "LUMBA"
text_area = label.Label(terminalio.FONT, text=text, background_tight=True, background_color=0x800000)
text_area.x = 0
text_area.y = text_area.bounding_box[3] // 3 * 2
text_area.scale = 2
text_area.flip_x = True
#text_area.flip_y = True
print(text_area.bounding_box)
group.append(text_area)
group.flip_x = True

while True:
    pass