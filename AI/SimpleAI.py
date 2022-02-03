import random


class SimpleAI:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def move(self, game_table):
        no_free_cell = True
        while no_free_cell:
            j = random.randint(0, self.max_x - 1)
            i = random.randint(0, self.max_y - 1)
            select_hex = game_table[j][i]
            if not select_hex.is_occupied() and select_hex.is_empty():
                return j, i
