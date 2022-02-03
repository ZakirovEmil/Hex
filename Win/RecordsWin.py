from Win.Win import Win
from FileСontroller import FileController
from tkinter import *


class RecordsWin(Win):
    def __init__(self):
        Win.__init__(self)

    def draw_records(self):
        records = FileController.load_records()
        if len(records) == 0:
            Label(self.root, text="Рекордов еще нет!", justify=LEFT, padx=15, pady=15) \
                .grid(row=0, column=0, sticky=W)
            return
        print(records)
        row = 0
        for record in records:
            Label(self.root, text=f"{record[0]}: {record[1]}", justify=LEFT, padx=15, pady=15)\
                .grid(row=row, column=0, sticky=W)
            row += 1

    def run(self):
        self.draw_records()
        self.root.mainloop()
