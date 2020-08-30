import pygame
import sys


class KeyboardEvents:
    def __init__(self):
        self.up_key = False
        self.down_key = False
        self.left_key = False
        self.right_key = False

    def get_direction(self):
        x = 0
        y = 0
        if self.up_key:
            y += -1
        if self.down_key:
            y += 1
        if self.left_key:
            x += -1
        if self.right_key:
            x += 1
        return [x, y]

    def set_events(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self.up_key = True
                if event.key == pygame.K_a:
                    self.left_key = True
                if event.key == pygame.K_s:
                    self.down_key = True
                if event.key == pygame.K_d:
                    self.right_key = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.up_key = False
                if event.key == pygame.K_a:
                    self.left_key = False
                if event.key == pygame.K_s:
                    self.down_key = False
                if event.key == pygame.K_d:
                    self.right_key = False


class TetrisPiece:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.keyboard_events = KeyboardEvents()
        self.ball = pygame.image.load("intro_ball.gif")
        self.ballrect = self.ball.get_rect()

    def move(self):

        eventos = pygame.event.get()
        self.keyboard_events.set_events(eventos)
        speed = self.keyboard_events.get_direction()

        if self.ballrect.left + speed[0] < 0 or self.ballrect.right + speed[0] > self.width or self.ballrect.top + speed[1] < 0 or self.ballrect.bottom + speed[1] > self.height:
            pass
        else:
            self.ballrect = self.ballrect.move(speed)