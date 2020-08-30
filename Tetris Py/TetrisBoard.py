import pygame
import sys

black = 0, 0, 0


class TetrisBoard:

    def __init__(self, size):
        self.screen = pygame.display.set_mode(size)

    def draw_board(self, ball, ballrect):
        self.screen.fill(black)
        self.screen.blit(ball, ballrect)
        pygame.display.flip()