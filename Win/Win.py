from tkinter import *


class Win:
    def __init__(self, weight=0, height=0, title="Hex", resizable=(False, False)):
        self.root = Tk()
        self.root.title(title)
        self.root.resizable(resizable[0], resizable[1])
