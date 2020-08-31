import pygame
import sys


class KeyboardEvents:
    def __init__(self):
        self.q_press = False
        self.w_press = False
        self.flag = "w"

    def get_direction(self):
        x = 0
        y = 0
        if self.q_press and self.flag == "w":
            x += 50
            self.q_press = False
        if self.w_press and self.flag == "q":
            x += 50
            self.w_press = False
        return [x, y]

    def set_events(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.q_press = True
                    self.flag = "q"
                if event.key == pygame.K_w:
                    self.w_press = True
                    self.flag = "w"


class Bola:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.keyboard_events = KeyboardEvents()
        self.ball = pygame.image.load("Imagenes/intro_ball.gif")
        self.ballrect = self.ball.get_rect()

    def move(self):
        win = False
        eventos = pygame.event.get()
        self.keyboard_events.set_events(eventos)
        speed = self.keyboard_events.get_direction()

        if self.ballrect.right + speed[0] > self.width:
            win = True
            return win
        else:
            self.ballrect = self.ballrect.move(speed)
            return win





