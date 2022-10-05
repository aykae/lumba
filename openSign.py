from matrix import Matrix
from text_display import TextDisplay
from backdrop import StarBackdrop

WIDTH = 64
HEIGHT = 32	
matrix = Matrix(width=WIDTH, height=HEIGHT, rotation=180)

font = 'IBMPlexMono-Medium-24.bdf'
td = TextDisplay(matrix, font, '0xFF0000')

td.drawText('OPEN', posx=0, posy=0, font_color='0xFFFFFF')
td.drawText('OPEN', posx=1, posy=1)

stars = StarBackdrop(matrix, delay=50, num_stars=25)

while True:
    stars.updateStars()
    matrix.display.refresh()