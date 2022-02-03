import math
from settings import *


class Hex:
    def __init__(self):
        self.width = math.sqrt(3) * SIZE_HEX
        self.height = SIZE_HEX * 2

    def get_shift_center(self, j, i, shift_x, shift_y):
        return self.width / 2 + self.width * j + shift_x, self.height / 2 + self.height * i - shift_y

    @staticmethod
    def get_hex_corner(cx, cy, i):
        angle = (math.pi / 3) * i - (math.pi / 6)
        return (cx + 2 + SIZE_HEX * math.cos(angle),
                cy + 2 + SIZE_HEX * math.sin(angle))
