# SPDX-FileCopyrightText: 2020 Melissa LeBlanc-Williams, written for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
================================================================================
Helper library for the MatrixPortal M4
* Author(s): Melissa LeBlanc-Williams
* Modified by AK Rai, Lumba Technologies

Implementation Notes
--------------------
**Hardware:**
* `Adafruit Matrix Portal <https://www.adafruit.com/product/4745>`_
**Software and Dependencies:**
* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

import board
import displayio
import rgbmatrix
import array

class Matrix:
    """Class representing the Adafruit RGB Matrix. This is used to automatically
    initialize the display.
    :param int width: The width of the display in Pixels. Defaults to 64.
    :param int height: The height of the display in Pixels. Defaults to 32.
    :param int bit_depth: The number of bits per color channel. Defaults to 2.
    :param list alt_addr_pins: An alternate set of address pins to use. Defaults to None
    :param string color_order: A string containing the letter "R", "G", and "B" in the
                               order you want. Defaults to "RGB"
    :param int width: The total width of the display(s) in Pixels. Defaults to 64.
    :param int height: The total height of the display(s) in Pixels. Defaults to 32.
    :param bool Serpentine: Used when panels are arranged in a serpentine pattern rather
                            than a Z-pattern. Defaults to True.
    :param int tiles_rows: Used to indicate the number of rows the panels are arranged in.
                           Defaults to 1.
    """

    # pylint: disable=too-few-public-methods,too-many-branches,too-many-statements,too-many-locals
    def __init__(
        self,
        *,
        width=64,
        height=32,
        bit_depth=2,
        alt_addr_pins=None,
        serpentine=True,
        tile_rows=1,
        rotation=0,
    ):
        panel_height = height // tile_rows
        self.rotation = rotation

        # MatrixPortal M4 Board
        addr_pins = [board.MTX_ADDRA, board.MTX_ADDRB, board.MTX_ADDRC]
        if panel_height > 16:
            addr_pins.append(board.MTX_ADDRD)
        if panel_height > 32:
            addr_pins.append(board.MTX_ADDRE)
        rgb_pins = [
            board.MTX_R1,
            board.MTX_G1,
            board.MTX_B1,
            board.MTX_R2,
            board.MTX_G2,
            board.MTX_B2,
        ]
        clock_pin = board.MTX_CLK
        latch_pin = board.MTX_LAT
        oe_pin = board.MTX_OE

        self.buffer = array.array('H') #an unsigned short array (16 bits)
        for i in range(width*height):
            self.buffer.append(int(0x0000))

        # Alternate Address Pins
        if alt_addr_pins is not None:
            addr_pins = alt_addr_pins

        try:
            displayio.release_displays()
            if tile_rows > 1:
                self.display = rgbmatrix.RGBMatrix(
                    width=width,
                    height=height,
                    bit_depth=bit_depth,
                    rgb_pins=(
                        rgb_pins[0],
                        rgb_pins[1],
                        rgb_pins[2],
                        rgb_pins[0 + 3],
                        rgb_pins[1 + 3],
                        rgb_pins[2 + 3],
                    ),
                    addr_pins=addr_pins,
                    clock_pin=clock_pin,
                    latch_pin=latch_pin,
                    output_enable_pin=oe_pin,
                    tile=tile_rows,
                    serpentine=serpentine,
                    framebuffer = self.buffer
                )
            else:
                self.display = rgbmatrix.RGBMatrix(
                    width=width,
                    height=height,
                    bit_depth=bit_depth,
                    rgb_pins=(
                        rgb_pins[0],
                        rgb_pins[1],
                        rgb_pins[2],
                        rgb_pins[0 + 3],
                        rgb_pins[1 + 3],
                        rgb_pins[2 + 3],
                    ),
                    addr_pins=addr_pins,
                    clock_pin=clock_pin,
                    latch_pin=latch_pin,
                    output_enable_pin=oe_pin,
                    framebuffer=self.buffer
                )
        except TypeError:
            if tile_rows > 1:
                raise RuntimeError(
                    "Make sure you are running CircuitPython 6.2.0.alpha-1 or later"
                ) from TypeError
            raise
        except ValueError:
            raise RuntimeError("Failed to initialize RGB Matrix") from ValueError
    
    def hexTo565(self, hex_color):
        converter = displayio.ColorConverter()
        c565 = converter.convert(int(hex_color, 16))
        return c565

    def setPixel(self, x, y, hex_color):
        color = self.hexTo565(hex_color)

        if self.rotation == 180:
            x = -1*(x - (self.display.width // 2 - 1)) + (self.display.width // 2 - 1)
            y = -1*(y - (self.display.height // 2 - 1)) + (self.display.height // 2 - 1)

        if 0 <= x < self.display.width and 0 <= y < self.display.height:
            self.buffer[(y * self.display.width) + x] = color

