import pygame
from Bola import Bola
from Board import Board


def main():
    pygame.init()
    size = width, height = 1080, 720
    bola1 = Bola(width, height)
    board = Board(size)

    while 1:
        win = bola1.move()
        board.draw_board(bola1.ball, bola1.ballrect)
        if win:
            font = pygame.font.Font('freesansbold.ttf', 60)
            mensaje = font.render("Ganaste gato", True, (0, 0, 0))
            mensaje_rect = mensaje.get_rect()
            mensaje_rect.center = (int((width/2)), int((height/2)))
            board.draw_board(mensaje, mensaje_rect)
            pygame.time.wait(3000)
            break


if __name__ == "__main__":
    main()
