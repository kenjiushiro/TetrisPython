import pygame
from pygame.color import THECOLORS


class Board:
    def __init__(self, size):
        pygame.display.set_caption('Juegazo')
        self.screen = pygame.display.set_mode(size)
        self.color = THECOLORS.get("lightblue3")

    def draw_board(self, ball, ballrect):
        self.screen.fill(self.color)
        self.screen.blit(ball, ballrect)
        pygame.display.flip()
