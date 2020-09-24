import random


class TetrisPiece:

    def __init__(self):
        self.__current_rotation = 0
        self.__get_new_piece()

    def __str__(self):
        return str(self.__this_piece)

    def __get_new_piece(self):
        self.__pieces = ["S", "Z", "L", "J", "T", "I", "O"]

        self.__dict_pieces = {"S": [["0...", "00..", ".0..", "...."], [".00.", "00..", "....", "...."]],
                              "Z": [[".0..", "00..", "0...", "...."], ["00..", ".00.", "....", "...."]],
                              "I": [[".0..", ".0..", ".0..", ".0.."], ["....", "0000", "....", "...."]],
                              "T": [[".0..", "000.", "....", "...."], [".0..", ".00.", ".0..", "...."],
                                    ["000.", ".0..", "....", "...."], [".0..", "00..", ".0..", "...."]],
                              "L": [["0...", "0...", "00..", "...."], ["000.", "0...", "....", "...."],
                                    ["00..", ".0..", ".0..", "...."], ["..0.", "000.", "....", "...."]],
                              "J": [[".0..", ".0..", "00..", "...."], ["0...", "000.", "....", "...."],
                                    ["00..", "0...", "0...", "...."], ["000.", "..0.", "....", "...."]],
                              "O": [["....", ".00.", ".00.", "...."]]}

        self.__dict_colors = {"S": (255, 128, 0),
                              "Z": (0, 255, 0),
                              "L": (0, 128, 255),
                              "J": (255, 0, 0),
                              "T": (0, 255, 128),
                              "I": (128, 0, 255),
                              "O": (255, 0, 255)}

        randomPiece = random.choice(self.__pieces)
        self.__this_piece = randomPiece
        self.__shapes = self.__dict_pieces[randomPiece]
        self.shape = self.__shapes[self.__current_rotation]
        self.color = self.__dict_colors[randomPiece]

    def next_rotation(self):
        return self.__shapes[0] if self.__current_rotation + 1 >= len(self.__shapes) else self.__shapes[self.__current_rotation + 1]

    def rotate(self):
        self.__current_rotation += 1
        if self.__current_rotation >= len(self.__shapes):
            self.__current_rotation = 0
        self.shape = self.__shapes[self.__current_rotation]

