import displayio

def rgbToHex(r, g, b):
    return "0x%02x%02x%02x" % (r, g, b)

def hexTo565(hex_color):
    converter = displayio.ColorConverter()
    c565 = converter.convert(int(hex_color, 16))
    return c565