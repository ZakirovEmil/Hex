from tkinter import *
from tkinter.ttk import Combobox

from FileСontroller import FileController
from Win.GameWin import GameWin
from Win.RecordsWin import RecordsWin
from settings import *
from Win.Win import Win


class StartWin(Win):
    def __init__(self):
        Win.__init__(self)
        self.select_mode = IntVar(0)
        self.name_1_entry = Entry(self.root)
        self.name_2_entry = Entry(self.root)
        self.mode_combobox = Combobox(self.root,
                                      values=(MODE_HOTSEAT, MODE_SIMPLE_AI, MODE_SMART_AI),
                                      state="readonly",
                                      justify=CENTER)
        self.size_table_combobox = Combobox(self.root,
                                            values=(SIZE_TABLE_6x6, SIZE_TABLE_11x11,
                                                    SIZE_TABLE_14x14, SIZE_TABLE_15x15),
                                            state="readonly",
                                            justify=CENTER)

    def create_game(self):
        GameWin(self.name_1_entry.get(), self.name_2_entry.get(),
                self.mode_combobox.get(), self.size_table_combobox.get(), (0, 0)).run()

    def load_game(self):
        game = FileController.load_game()
        game_win = GameWin(game[5], game[6], game[1], game[7], True)
        game_win.run()

    def show_records(self):
        RecordsWin().run()

    def draw_widgets(self):
        Label(self.root, text="Name 1:", justify=LEFT).grid(row=0, column=0, sticky=W)
        self.name_1_entry.grid(row=0, column=1, sticky=W + E, padx=5, pady=5)

        Label(self.root, text="Name 2:", justify=LEFT).grid(row=1, column=0, sticky=W)
        self.name_2_entry.grid(row=1, column=1, sticky=W + E, padx=5, pady=5)

        Label(self.root, text="Mode:", justify=LEFT).grid(row=2, column=0, sticky=W)
        self.mode_combobox.grid(row=2, column=1, sticky=W + E, padx=5, pady=5)

        Label(self.root, text="Size table:", justify=LEFT).grid(row=3, column=0, sticky=W)
        self.size_table_combobox.grid(row=3, column=1, sticky=W + E, padx=5, pady=5)

        Button(self.root, text="Play!", width=10, command=self.create_game) \
            .grid(row=4, column=0, columnspan=2, padx=5, sticky=E + W)
        Button(self.root, text="Records", width=10, command=self.show_records) \
            .grid(row=5, column=0, columnspan=2, padx=5, sticky=E + W)
        Button(self.root, text="Load game", width=10, command=self.load_game) \
            .grid(row=6, column=0, columnspan=2, padx=5, sticky=E + W)

    def run(self):
        self.draw_widgets()
        self.root.mainloop()


if __name__ == "__main__":
    root = StartWin()
    root.run()
