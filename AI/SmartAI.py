import random
from settings import *
from Cell import Cell


class SmartAI:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.first_step = True
        self.path = dict()
        self.last_cell = (0, 0)
        self.color = SECOND_COLOR
        self.prev_cell = (0, 0)

    def get_next_cells(self, x, y, table):
        check_next_node = lambda x, y: True if 0 <= x < self.max_x and \
                                               0 <= y < self.max_y else False
        ways = [1, 0], [0, 1], [1, -1]
        return [table[x + dx][y + dy] for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def move(self, game_table):
        if self.first_step:
            while True:
                self.first_step = False
                j = 0
                i = random.randint(0, self.max_y - 1)
                select_hex = game_table[j][i]
                if not select_hex.is_occupied() and select_hex.is_empty():
                    self.path[select_hex] = [None]
                    self.last_cell = select_hex
                    return select_hex.x, select_hex.y
        else:
            self.prev_cell = self.last_cell
            next_cell = self.get_next_cells(self.last_cell.x, self.last_cell.y, game_table)
            select_cell = None
            # for cell in next_cell:
            #     self.path[cell] = list()
            for cell in next_cell:
                if not cell.is_occupied() and cell.is_empty():
                    # self.path[cell].append(self.last_cell)
                    self.path[cell] = self.last_cell
                    if not select_cell:
                        select_cell = cell
            if not select_cell:
                select_cell = self.last_cell
                search_cell = True
                while search_cell:
                    select_cell = self.path.get(select_cell)
                    next_cell = self.get_next_cells(select_cell.x, select_cell.y, game_table)
                    for cell in next_cell:
                        if not cell.is_occupied() and cell.is_empty():
                            search_cell = False
                            select_cell = cell
                            break
            self.last_cell = select_cell
            return self.last_cell.x, self.last_cell.y