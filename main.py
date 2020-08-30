import sys
import pygame
from TetrisPiece import KeyboardEvents, TetrisPiece
from TetrisBoard import TetrisBoard
from pygame.color import THECOLORS

print(THECOLORS.get("red"))


def main():
    pygame.init()
    size = width, height = 1280, 720

    tetris_piece = TetrisPiece(width, height)
    tetris_board = TetrisBoard(size)

    while 1:
        tetris_piece.move()
        tetris_board.draw_board(tetris_piece.ball, tetris_piece.ballrect)
# IMPECABLE PAPA

if __name__ == "__main__":
    main()
