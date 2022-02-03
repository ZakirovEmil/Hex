from Win.Win import Win
from tkinter import *
from Game import Game
from settings import *
from FileСontroller import FileController


class GameWin(Win):
    def __init__(self, name_1, name_2, mode, size_game, load_game=False):
        Win.__init__(self)
        if load_game == True:
            print("1")
            self.game = Game(self.root, name_1, name_2, mode, size_game, (0,0), True)
        else:
            self.game = Game(self.root, name_1, name_2, mode, size_game)
        self.show_winner = False

    def draw_game(self):
        self.game.canvas.grid(row=0, column=0, rowspan=4)

    def draw_game_panel(self):
        Label(self.root, text=f"{self.game.score[0]} : {self.game.score[1]}",
              padx=10, pady=10) \
            .grid(row=0, column=1, sticky=N)
        Button(self.root, text="Undo", width=10, command=self.on_undo) \
            .grid(row=1, column=1, sticky=E + W + N)
        Button(self.root, text="Redo", width=10, command=self.on_redo) \
            .grid(row=2, column=1, sticky=E + W + N)
        Button(self.root, text="Save", width=10, command=self.on_save) \
            .grid(row=3, column=1, sticky=E + W + N)

    def draw(self):
        self.draw_game()
        self.draw_game_panel()

    def on_undo(self):
        self.game.make_undo()

    def on_redo(self):
        self.game.make_redo()

    def on_save(self):
        self.game.save_game()

    def on_close(self):
        if self.game.mode == MODE_SMART_AI or self.game.mode == MODE_SIMPLE_AI:
            FileController.save_records(((self.game.name_1, self.game.score[0]),))
        else:
            FileController.save_records(((self.game.name_1, self.game.score[0]),
                                         (self.game.name_2, self.game.score[1])))
        self.root.destroy()

    def draw_how_win(self, color):
        self.game.canvas.create_text(0, self.game.size_canvas[1], text=f"{color} win!!!",
                                     anchor=SW, fill="grey")
        self.draw_game()

    def check_win(self):
        if self.game.game_over[0] and not self.show_winner:
            print(self.game.game_over[1] + "WIN")
            print(self.game.game_over[1])
            self.game.score = (self.game.score[0] + 1, self.game.score[1]) \
                if self.game.game_over[1] == FIRST_COLOR \
                else (self.game.score[0], self.game.score[1] + 1)
            print(self.game.score, "!!!!!!!!!")
            self.draw_how_win(self.game.game_over[1])
            self.root.after(5000, self.create_new_game, Game(self.root, self.game.name_1,
                                                             self.game.name_2, self.game.mode,
                                                             self.game.size_game, self.game.score))
            self.show_winner = True
        self.root.after(1, self.check_win)

    def create_new_game(self, game):
        self.show_winner = False
        self.game = game
        self.draw()

    def run(self):
        self.draw()
        self.root.after(1, self.check_win)
        self.root.protocol('WM_DELETE_WINDOW', self.on_close)
        self.root.mainloop()

# if __name__ == "__main__":
#     GameWin("").run()
