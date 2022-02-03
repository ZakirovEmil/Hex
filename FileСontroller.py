import pickle
import shelve
from settings import *


class FileController:
    @staticmethod
    def save_game(game):
        with open(PATH_SAVE_GAME, 'wb') as save_game:
            print("Сохранил")
            pickle.dump([game.table, game.mode, game.AI, game.score,
                         game.color, game.name_1, game.name_1,
                         game.size_game], save_game, protocol=2)

    @staticmethod
    def load_game():
        with open(PATH_SAVE_GAME, 'rb') as save_game:
            # print(pickle.load(save_game))
            return pickle.load(save_game)

    @staticmethod
    def load_records():
        result = list()
        with shelve.open(PATH_RECORDS, 'c') as records:
            for name in records.keys():
                print((name, records[name]))
                result.append((name, records[name]))
        print(result)
        return sorted(result, key=lambda i: i[1], reverse=True)

    @staticmethod
    def save_records(new_records):
        with shelve.open(PATH_RECORDS, 'c') as records:
            for record in new_records:
                print(new_records)
                records[record[0]] = records.get(record[0], 0) + int(record[1])
