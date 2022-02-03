from settings import *


class Cell:
    def __init__(self, identifier, x=0, y=0, color=EMPTY):
        self.identifier = identifier
        self.color = color
        self.x = x
        self.y = y
        self.tag = TAG

    def is_occupied(self):
        return self.color != EMPTY

    def is_empty(self):
        return self.color == EMPTY
