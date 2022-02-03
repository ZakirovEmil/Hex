from collections import deque
from tkinter import *
from settings import *
from Cell import Cell
from Hex import Hex
from AI.SmartAI import SmartAI
from AI.SimpleAI import SimpleAI
from FileСontroller import FileController


class Game:
    def __init__(self, root, name_1, name_2, mode, table_size, score=(0, 0), load_game=False):
        self.root = root
        self.mode = mode
        self.name_1 = name_1
        self.name_2 = name_2
        self.score = score
        self.size_game = table_size
        self.table_height = SIZE_TABLE.get(table_size)[0]
        self.table_width = SIZE_TABLE.get(table_size)[1]
        self.size_canvas = SIZE_CANVAS.get(table_size)
        self.color = FIRST_COLOR
        self.tag = TAG
        self.hex = Hex()
        self.game_over = (False, EMPTY)
        self.canvas = self.create_canvas()
        self.table = self.create_table()
        self.last_move_undo = deque()
        self.last_move_redo = deque()
        if mode == MODE_SIMPLE_AI:
            self.AI = SimpleAI(self.table_width, self.table_height)
        elif mode == MODE_SMART_AI:
            self.AI = SmartAI(self.table_width, self.table_height)
        else:
            self.AI = None
        if load_game == True:
            self.load_game()
        self.draw_table()

    def save_game(self):
        FileController.save_game(self)

    def load_game(self):
        stats = FileController.load_game()
        self.table = stats[0]
        self.mode = stats[1]
        self.AI = stats[2]
        self.score = stats[3]
        self.color = stats[4]
        self.name_1 = stats[5]
        self.name_2 = stats[6]
        self.size_game = stats[7]

    def create_canvas(self):
        return Canvas(self.root, width=self.size_canvas[0],
                      height=self.size_canvas[1],
                      bg='white')

    def move_next(self):
        self.color = SECOND_COLOR if self.color == FIRST_COLOR else FIRST_COLOR

    def make_undo(self):
        if len(self.last_move_undo) != 0:
            if self.mode == MODE_SIMPLE_AI or self.mode == MODE_SMART_AI:
                last_hex = self.last_move_undo.pop()
                prev_hex = self.last_move_undo.pop()
                self.last_move_redo.appendleft(last_hex)
                self.last_move_redo.appendleft(prev_hex)
                if self.AI == MODE_SMART_AI:
                    self.AI.last_cell = self.AI.prev_cell
                print(last_hex)
                print(prev_hex)
                self.table[last_hex.x][last_hex.y] = Cell(last_hex.identifier,
                                                          last_hex.x, last_hex.y)
                self.table[prev_hex.x][prev_hex.y] = Cell(prev_hex.identifier,
                                                          prev_hex.x, prev_hex.y)
                self.canvas.itemconfig(last_hex.identifier,
                                       tag=TAG)
                self.canvas.itemconfig(prev_hex.identifier,
                                       tag=TAG)
                self.canvas.itemconfig(TAG, fill=EMPTY,  activefill=self.color)

            else:
                last_hex = self.last_move_undo.pop()
                self.last_move_redo.appendleft(last_hex)
                self.table[last_hex.x][last_hex.y] = Cell(last_hex.identifier,
                                                          last_hex.x, last_hex.y)
                self.color = last_hex.color
                # self.canvas.itemconfig(last_hex.identifier, fill=EMPTY,
                #                        tag="hex", activefill=last_hex.color)

                self.canvas.itemconfig(last_hex.identifier,
                                       tag=TAG)
                self.canvas.itemconfig(self.tag, fill=EMPTY, activefill=self.color)

    def make_redo(self):
        if len(self.last_move_redo) != 0:
            if self.mode == MODE_SIMPLE_AI and MODE_SMART_AI:
                prev_hex = self.last_move_redo.popleft()
                last_hex = self.last_move_redo.popleft()
                self.table[last_hex.x][last_hex.y] = Cell(last_hex.identifier,
                                                          last_hex.x, last_hex.y)
                self.table[last_hex.x][last_hex.y].color = last_hex.color
                # print(last_hex.x, last_hex.y, last_hex.color, self.table[last_hex.x][last_hex.y].color)
                self.table[prev_hex.x][prev_hex.y] = Cell(prev_hex.identifier,
                                                          prev_hex.x, prev_hex.y)
                self.table[last_hex.x][last_hex.y].color = prev_hex.color

                self.canvas.itemconfig(prev_hex.identifier, fill=prev_hex.color,
                                       tag=last_hex.color, activefill=prev_hex.color)
                self.canvas.itemconfig(last_hex.identifier, fill=last_hex.color,
                                       tag=last_hex.color, activefill=last_hex.color)
                self.color = prev_hex.color
                self.canvas.itemconfig(self.tag, activefill=self.color)
            else:
                last_hex = self.last_move_redo.popleft()
                self.table[last_hex.x][last_hex.y] = Cell(last_hex.identifier,
                                                          last_hex.x, last_hex.y)
                self.table[last_hex.x][last_hex.y].color = last_hex.color

                self.move_next()
                self.canvas.itemconfig(last_hex.identifier, fill=last_hex.color,
                                       tag=last_hex.color, activefill=last_hex.color)

    def draw_table(self):
        shift_x = 0
        shift_y = 0
        for i in range(0, self.table_height):
            for j in range(0, self.table_width):
                corners = list()

                for corner in range(0, 6):
                    center = self.hex.get_shift_center(j, i, shift_x, shift_y)
                    corners.append(self.hex.get_hex_corner(center[0], center[1], corner))

                identifier = self.canvas.create_polygon(corners[0][0], corners[0][1],
                                                        corners[1][0], corners[1][1],
                                                        corners[2][0], corners[2][1],
                                                        corners[3][0], corners[3][1],
                                                        corners[4][0], corners[4][1],
                                                        corners[5][0], corners[5][1],
                                                        fill=self.table[j][i].color, outline='black',
                                                        activefill=self.table[j][i].color,
                                                        tag=self.table[j][i].tag)

                self.check_border(j, i, corners)
                self.table[j][i].identifier = identifier
                self.canvas.tag_bind(identifier, "<Button-1>", lambda event, pic=identifier: self.on_click(pic))

            shift_x += self.hex.width / 2
            shift_y += self.hex.height / 4

    def create_table(self):
        table = [[Cell(None) for i in range(self.table_height)] for i in range(self.table_width)]
        for i in range(0, self.table_height):
            for j in range(0, self.table_width):
                table[j][i] = Cell(None, j, i)
        return table

    def create_border_line(self, line_1, line_2, color):
        self.canvas.create_line(line_1[0], line_1[1], line_1[2], line_1[3], width=3, fill=color)
        self.canvas.create_line(line_2[0], line_2[1], line_2[2], line_2[3], width=3, fill=color)

    def check_border(self, j, i, corners):
        if i == 0:
            line = [[corners[4][0], corners[4][1], corners[5][0], corners[5][1]],
                    [corners[0][0], corners[0][1], corners[5][0], corners[5][1]],
                    FIRST_COLOR]
            if j == self.table_width - 1:
                line[1][0] = line[1][0] - self.hex.width / 4,
                line[1][1] = line[1][1] - self.hex.height / 8,
            self.create_border_line(line[0], line[1], line[2])
        if i == self.table_width - 1:
            line = [[corners[2][0], corners[2][1], corners[3][0], corners[3][1]],
                    [corners[1][0], corners[1][1], corners[2][0], corners[2][1]],
                    FIRST_COLOR]
            if j == 0:
                line[0][2] = line[0][2] + self.hex.width / 4,
                line[0][3] = line[0][3] + self.hex.height / 8,
            self.create_border_line(line[0], line[1], line[2])

        if j == 0:
            line = [[corners[2][0], corners[2][1], corners[3][0], corners[3][1]],
                    [corners[3][0], corners[3][1], corners[4][0], corners[4][1]],
                    SECOND_COLOR]
            if i == self.table_width - 1:
                line[0][0] = line[0][0] - self.hex.width / 4,
                line[0][1] = line[0][1] - self.hex.height / 8,
            self.create_border_line(line[0], line[1], line[2])
        if j == self.table_width - 1:
            line = [[corners[5][0], corners[5][1], corners[0][0], corners[0][1]],
                    [corners[0][0], corners[0][1], corners[1][0], corners[1][1]],
                    SECOND_COLOR]
            if i == 0:
                line[0][0] = line[0][0] + self.hex.width / 4,
                line[0][1] = line[0][1] + self.hex.height / 8,
            self.create_border_line(line[0], line[1], line[2])

    def check_win(self):
        # print("check_win")
        # print(self.color)
        for i in range(self.table_width):
            x = (i if self.color == FIRST_COLOR else 0)
            y = (0 if self.color == FIRST_COLOR else i)
            if self.color == self.table[x][y].color:
                cur_cell = self.table[x][y]
                queue = deque([cur_cell])
                visited = set()
                while queue:
                    cur_cell = queue.pop()
                    visited.add(cur_cell)
                    if cur_cell.color == FIRST_COLOR and cur_cell.y == self.table_width - 1 or \
                            cur_cell.color == SECOND_COLOR and cur_cell.x == self.table_width - 1:
                        [self.canvas.itemconfig(cell.identifier, fill="red") for cell in visited]
                        self.game_over = (True, self.color)
                        return
                    next_cells = self.get_next_cells(cur_cell.x, cur_cell.y, self.color)
                    for next_cell in next_cells:
                        if next_cell not in visited and self.color == next_cell.color:
                            queue.append(next_cell)

    def get_next_cells(self, x, y, color):
        check_next_node = lambda x, y: True if 0 <= x < self.table_width and \
                                               0 <= y < self.table_height else False
        ways = [-1, 0], [1, 0], [0, -1], [0, 1], [1, -1], [-1, 1]
        return [self.table[x + dx][y + dy] for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def set_color_cell(self, j, i, color):
        self.table[j][i].color = self.color
        self.table[j][i].tag = self.color
        self.canvas.itemconfig(self.table[j][i].identifier, fill=self.table[j][i].color,
                               activefill=self.table[j][i].color,
                               tag=self.table[j][i].color)
        print(self.table[j][i].color, j, i, self.table[j][i].x, self.table[j][i].y)

    def move_AI(self):
        cell = self.AI.move(self.table)
        self.set_color_cell(cell[0], cell[1], self.color)
        print(self.table[cell[0]][cell[1]].color, cell[0], cell[1],
              self.table[cell[0]][cell[1]].x, self.table[cell[0]][cell[1]].y)
        self.check_win()
        self.last_move_undo.append(self.table[cell[0]][cell[1]])
        self.move_next()
        self.canvas.itemconfig(self.tag, activefill=self.color)

    def on_click(self, pic):
        for i in range(self.table_height):
            for j in range(self.table_width):
                select_hex = self.table[j][i]
                if select_hex.identifier == pic:
                    # print(select_hex.color)
                    # print(select_hex.x, select_hex.y)
                    if not select_hex.is_occupied() and select_hex.is_empty():
                        self.last_move_undo.append(select_hex)
                        self.table[j][i].color = self.color
                        self.table[j][i].tag = self.color
                        self.set_color_cell(j, i, self.color)
                        # self.canvas.itemconfig(pic, fill=self.table[j][i].color,
                        #                        tag=self.table[j][i].color)
                        # print(self.table[j][i].color, j, i, self.table[j][i].x, self.table[j][i].y)
                        # print(j, i, self.color)
                        self.check_win()
                        self.move_next()
                        if self.mode == MODE_SIMPLE_AI or self.mode == MODE_SMART_AI:
                            self.move_AI()
                        self.canvas.itemconfig(self.tag, activefill=self.color)
                        return

    def draw_test(self):
        self.canvas.pack()

    def run_test(self):
        self.draw_test()
        # self.root.after(1, self.check_win())
        self.root.mainloop()


if __name__ == "__main__":
    Game(Tk(), MODE_HOTSEAT, SIZE_TABLE_6x6).run_test()
