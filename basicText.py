from matrix import Matrix
from text_display import TextDisplay

WIDTH = 64
HEIGHT = 32	
matrix = Matrix(width=WIDTH, height=HEIGHT, rotation=180)

font = 'IBMPlexMono-Medium-24.bdf'
td = TextDisplay(matrix, font, '0xFF0000')

td.drawText('LUMBA')

while True:
    matrix.display.refresh()