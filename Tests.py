import unittest
from Game import Game
from tkinter import *
from settings import *
from Cell import Cell


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.game = Game(Tk(), "Oleg", "Denis", MODE_SMART_AI, SIZE_TABLE_6x6, (0, 0))

    def test_name_1(self):
        self.assertEqual(self.game.name_1, "Oleg")

    def test_name_2(self):
        self.assertEqual(self.game.name_2, "Denis")

    def test_select_AI(self):
        self.assertNotEqual(self.game.AI, None)

    def test_check_win(self):
        self.game.check_win()
        self.assertEqual(self.game.game_over[0], False)

    def test_win_first(self):
        self.game.table_width = 3
        self.game.table_height = 3
        self.game.color = FIRST_COLOR
        self.game.table = \
            [
                [Cell("", 0, 0), Cell("", 0, 1), Cell("", 0, 2)],
                [Cell("", 1, 0, FIRST_COLOR), Cell("", 1, 1, FIRST_COLOR), Cell("", 1, 2, FIRST_COLOR)],
                [Cell("", 2, 0), Cell("", 2, 1), Cell("", 2, 2)]
            ]
        self.game.check_win()
        self.assertEqual(self.game.game_over[0], True)
        self.assertEqual(self.game.game_over[1], FIRST_COLOR)

    def test_win_second(self):
        self.game.table_width = 3
        self.game.table_height = 3
        self.game.color = SECOND_COLOR
        self.game.table = \
            [
                [Cell("", 0, 0), Cell("", 0, 1, SECOND_COLOR), Cell("", 0, 2)],
                [Cell("", 1, 0), Cell("", 1, 1, SECOND_COLOR), Cell("", 1, 2)],
                [Cell("", 2, 0), Cell("", 2, 1, SECOND_COLOR), Cell("", 2, 2)]
            ]
        self.game.check_win()
        self.assertEqual(self.game.game_over[0], True)
        self.assertEqual(self.game.game_over[1], SECOND_COLOR)


if __name__ == '__main__':
    unittest.main()
