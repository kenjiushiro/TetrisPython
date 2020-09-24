# from numpy.core import string_

from TetrisPiece import TetrisPiece
import random
import pygame
from pygame.locals import *
import sys
import os

BACKGROUND_COLOR = 25, 25, 15
WHITE = 255, 255, 255
BLACK = 0, 0, 0
LINE_COLOR = 128, 128, 128

GRAVITY = USEREVENT + 1
GAME_TICK = USEREVENT + 2
KEYPRESSED = USEREVENT + 3
STARTKEY = USEREVENT + 4
ESCKEY = USEREVENT + 5
# FONTNAME = 'Comic Sans MS'
FONTNAME = 'Consolas'


class TetrisGame:

    def __init__(self, rows=20, columns=10, block_length=40, border_width=20):
        pygame.init()
        print(pygame.display.Info())
        pygame.display.set_caption('Tetris')
        icon = pygame.image.load('images\\tetrisIcon.png')
        pygame.display.set_icon(icon)
        pygame.font.init()

        self.falling_intervals = {1: 700, 2: 600, 3: 500, 4: 400, 5: 300, 6: 200, 7: 150}
        self.level_thresholds = {1: 15, 2: 30, 3: 50, 4: 70, 5: 95, 6: 120, 7: 150}
        self.level_score_multiplier = {1: 1, 2: 1.2, 3: 1.4, 4: 1.6, 5: 1.8, 6: 2, 7: 2.2}

        self.block_length = block_length
        self.rows_count = rows
        self.columns_count = columns

        borders = border_width
        self.height = rows * self.block_length
        height = self.height + borders * 2
        self.width = columns * self.block_length
        width = self.width + block_length * 4 + borders * 3
        size = width, height
        self.screen = pygame.display.set_mode(size)#,FULLSCREEN)

        self.top_left_x = self.top_left_y = borders

        self.next_piece_top_left_x = borders * 2 + self.width
        self.next_piece_top_left_y = borders

        self.playing_rect = pygame.Rect((self.top_left_x, self.top_left_y), (self.width, self.height))

        next_piece_topleft = self.playing_rect.topright[0] + borders, self.playing_rect.topright[1]

        square_size4 = block_length * 4, block_length * 4
        square_size6 = block_length * 6, block_length * 6
        self.next_piece_rect = pygame.Rect(next_piece_topleft, square_size4)

        score_topleft = self.next_piece_rect.bottomleft[0], self.next_piece_rect.bottomleft[1] + borders

        self.score_rect = pygame.Rect(score_topleft, square_size4)
        instructions_topleft = self.score_rect.bottomleft[0], self.score_rect.bottomleft[1] + borders
        self.instructions_rect = pygame.Rect(instructions_topleft, square_size6)
        hiscore_topleft = self.instructions_rect.bottomleft[0], self.instructions_rect.bottomleft[1] + borders
        self.hiscore_rect = pygame.Rect(hiscore_topleft, square_size4)

        self.spawn_position = 4, 0
        self.keyboard_events = KeyboardEvents()

    def spawn_piece(self, tetris_piece: TetrisPiece):
        color = tetris_piece.color
        string_list = self.convert_string_list_to_grid(tetris_piece.shape, self.spawn_position)
        self.current_piece_position = string_list
        if self.can_spawn(string_list):
            self.change_coords_color(string_list, color)
            return True
        else:
            return False

    def can_spawn(self, string_list):
        for coord in string_list:
            if self.grid_color(coord) != BACKGROUND_COLOR:
                return False
        return True

    def grid_color(self, coord):
        x, y = coord
        return self.grid[y][x]

    @staticmethod
    def convert_string_list_to_grid(current_shape_string_list, spawn_position):
        sx, sy = spawn_position
        stringlist = []
        for line in range(len(current_shape_string_list)):
            for column in range(len(current_shape_string_list[line])):
                if current_shape_string_list[line][column] == "0":
                    stringlist.append((sx + column, sy + line))
        return stringlist

    def show_next_piece(self):
        self.next_piece = TetrisPiece()
        pygame.draw.rect(self.screen, BACKGROUND_COLOR, self.next_piece_rect)
        self.draw_piece(self.next_piece, 0, 0, self.__get_top_left_next_piece)
        self.draw_next_piece_grid()
        pygame.display.update(self.next_piece_rect)

    def draw_piece(self, piece: TetrisPiece, x, y, coords_funct):
        color = piece.color
        for linea in range(len(piece.shape)):
            for columna in range(len(piece.shape[linea])):
                if piece.shape[linea][columna] == "0":
                    cuadrado = self.draw_square(y + linea, x + columna, color, coords_funct)

    def draw_square(self, line, column, color, coords_funct):
        sx, sy = coords_funct(column, line)
        return pygame.draw.rect(self.screen, color, pygame.Rect(sx, sy, self.block_length, self.block_length))

    def check_for_full_rows(self):
        lines_count = 0
        while self.clear_full_row():
            lines_count += 1
        if lines_count > 0:
            self.update_score(lines_count)

    def get_score(self, rows_cleared):
        score = 0
        if rows_cleared == 1:
            score = 100
        elif rows_cleared == 2:
            score = 250
        elif rows_cleared == 3:
            score = 750
        elif rows_cleared == 4:
            score = 1500
        score *= self.level_score_multiplier[self.level]
        return int(score)

    def update_score(self, lines_count):
        # print("Score:" + str(self.score))
        # print("Lines cleared:" + str(self.lines_cleared))
        # print("Level: " + str(self.level))
        self.score += self.get_score(lines_count)
        self.lines_cleared += lines_count
        self.show_level()
        self.show_score()
        if self.lines_cleared > self.level_thresholds[self.level] and self.level <= len(self.level_thresholds):
            self.level += 1

            self.falling_interval = self.falling_intervals[self.level]
            self.set_gravity()

    def show_score(self):
        self.show_list(["Score", str(self.score)], self.score_rect)

    def show_level(self):
        self.show_list(["Level", str(self.level), "(" + str(self.lines_cleared) + ")"], self.hiscore_rect)

    def show_hiscore(self):
        self.show_list(["HiScore", str(self.hiscore)], self.hiscore_rect)

    def show_list(self, string_list, rect):
        myfont = pygame.font.SysFont(FONTNAME, 30)

        surface_list = [myfont.render(palabra, False, WHITE) for palabra in string_list]
        pygame.draw.rect(self.screen, (0, 0, 0), rect)

        text_position = rect.topleft
        for surface in surface_list:
            self.screen.blit(surface, text_position)
            text_position = text_position[0], text_position[1] + 30
        pygame.display.update(rect)

    def show_instructions(self):
        self.show_list(["Press", "Enter:", "Start", "Esc: ", "End Game"], self.instructions_rect)

    def increase_falling_speed(self):
        if self.lines_cleared > self.level_thresholds[self.level]:
            self.level += 1
        self.falling_interval = self.falling_intervals[self.level]

    def clear_full_row(self):
        linea_vacia = [BACKGROUND_COLOR for x in range(self.columns_count)]
        for i in range(19, -1, -1):
            if BACKGROUND_COLOR not in self.grid[i]:
                i += 1
                self.grid[1:i] = self.grid[0:i-1]
                self.grid[0] = linea_vacia
                return True
        return False

    def __create_grid(self):
        rows = self.rows_count
        columns = self.columns_count
        self.grid = [[BACKGROUND_COLOR for _ in range(columns)] for _ in range(rows)]

    def __get_top_left(self, x, y):
        sx = self.top_left_x + x * self.block_length
        sy = self.top_left_y + y * self.block_length
        return sx, sy

    def __get_top_left_next_piece(self, x, y):
        sx = self.next_piece_top_left_x + x * self.block_length
        sy = self.next_piece_top_left_y + y * self.block_length
        return sx, sy

    def __draw_grid_lines(self):
        sx = self.top_left_x
        sy = self.top_left_y
        block_size = self.block_length
        grid_height = self.rows_count * block_size
        grid_width = self.columns_count * self.block_length

        for row in range(self.rows_count + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (sx, sy + row * block_size),
                             (sx + grid_width, sy + row * block_size))
        for column in range(self.columns_count + 1):
            pygame.draw.line(self.screen, LINE_COLOR, (sx + column * block_size, sy),
                             (sx + column * block_size, sy + grid_height))

    def draw_next_piece_grid(self):
        sx = self.next_piece_top_left_x
        sy = self.next_piece_top_left_y
        block_size = self.block_length
        for i in range(5):
            pygame.draw.line(self.screen, LINE_COLOR, (sx, sy + i * block_size),
                             (sx + 4 * block_size, sy + i * block_size))
        for j in range(5):
            pygame.draw.line(self.screen, LINE_COLOR, (sx + j * block_size, sy),
                             (sx + j * block_size, sy + 4 * block_size))

    def __draw_grid(self):
        for line in range(len(self.grid)):
            for column in range(len(self.grid[line])):
                color = self.grid[line][column]
                self.draw_square(line, column, color, self.__get_top_left)

    def move_piece(self, speed):
        x_speed = speed[0], 0
        y_speed = 0, speed[1]
        if y_speed != (0, 0):
            for i in range(y_speed[1]):
                y_speed = (0, 1)
                if self.can_move(y_speed):
                    self.move_by(y_speed)
                else:
                    if self.get_new_piece():
                        break
                    else:
                        return False
            if self.can_move(y_speed) and y_speed == (0, -1):
                self.rotate()
        if x_speed != (0, 0) and self.can_move(x_speed):
            self.move_by(x_speed)
        return True

    def move_by(self, y_speed):
        new_position = [(x + y_speed[0], y + y_speed[1]) for (x, y) in self.current_piece_position]
        self.change_coords_color(self.current_piece_position, BACKGROUND_COLOR)
        self.current_piece_position = new_position
        self.change_coords_color(self.current_piece_position, self.active_piece.color)

    def rotate(self):
        self.change_coords_color(self.current_piece_position, BACKGROUND_COLOR)
        top_left = self.get_top_left()
        new_position = self.convert_string_list_to_grid(self.active_piece.next_rotation(), top_left)
        self.active_piece.rotate()
        self.current_piece_position = new_position
        self.change_coords_color(self.current_piece_position, self.active_piece.color)

    def get_new_piece(self):
        self.check_for_full_rows()
        self.active_piece = self.next_piece
        if self.spawn_piece(self.active_piece):
            self.show_next_piece()
            return True
        else:
            return False

    def can_move(self, speed):
        border_coords = self.get_border_coords(speed)
        for column, line in border_coords:
            if line >= self.rows_count or column >= self.columns_count or line < 0 or column < 0:
                return False
            if self.grid[line][column] != BACKGROUND_COLOR:
                return False
        return True

    def get_border_coords(self, speed):
        border_coords = []
        if speed != (0, 0):
            if speed == (0, -1):
                top_left = self.get_top_left()
                border_coords = self.convert_string_list_to_grid(self.active_piece.next_rotation(), top_left)
            else:
                for coord in self.current_piece_position:
                    border_coords.append((coord[0] + speed[0], coord[1] + speed[1]))
        border_coords = [item for item in border_coords if item not in self.current_piece_position]
        return border_coords

    def get_top_left(self):
        top_x = 20
        top_y = 20
        for x, y in self.current_piece_position:
            if x < top_x:
                top_x = x
            if y < top_y:
                top_y = y
        return top_x, top_y

    def change_coords_color(self, coords_list, color):
        for coord in coords_list:
            line = coord[1]
            column = coord[0]
            self.grid[line][column] = color

    def start_game(self):
        self.draw_start_screen()
        while 1:
            eventos = pygame.event.get()
            for event in eventos:

                self.keyboard_events.set_events(eventos)
                if event.type == MOUSEBUTTONDOWN:
                    self.change_grid_color_onclick(event)
                if event.type == STARTKEY:
                    self.new_game()
                if event.type == ESCKEY:
                    return

    def change_grid_color_onclick(self, event):
        pos = event.pos
        if event.button == 1:
            color = TetrisPiece().color
        # elif event.button == 3:
        else:
            color = BACKGROUND_COLOR
        x, y = pos
        if self.top_left_x < x < self.top_left_x + self.width and \
                self.top_left_y < y < self.height:

            x -= self.top_left_x
            y -= self.top_left_y
            x /= self.block_length
            y /= self.block_length
            x = int(x)
            y = int(y)
            self.grid[y][x] = color
            self.draw_board()

    def draw_start_screen(self):
        rows = self.rows_count
        columns = self.columns_count

        self.screen.fill(BLACK)
        pygame.display.flip()
        self.__create_grid()

        for row in range(5, 9):
            for col in range(1, columns - 1):
                random_color = TetrisPiece().color
                self.grid[row][col] = random_color
        for row in range(9, rows - 3):
            for col in range(3, columns - 3):
                random_color = TetrisPiece().color
                self.grid[row][col] = random_color
        self.show_hiscore()
        self.show_list(["Enter:", "Start Game", "", "Esc: ", "Exit"], self.instructions_rect)

        self.draw_board()

    def game_over_animation(self):
        rows = self.rows_count
        columns = self.columns_count
        speed = 8
        myfont = pygame.font.SysFont(FONTNAME, 30)
        gameover_text = "GAME OVER"
        gameover_surface = myfont.render(gameover_text, False, WHITE)
        topleft = self.width / 4, self.height / 4
        size = self.width / 2, self.height / 10
        gameover_rect = pygame.Rect(topleft, size)
        pygame.draw.rect(self.screen, (0, 0, 0), gameover_rect)

        for row in range(rows - 1, -1, -1):
            for col in range(0, columns):
                random_color = TetrisPiece().color
                # """
                self.grid[row][col] = random_color
                self.draw_board()
                """
                self.draw_square(row, col, random_color, self.__get_top_left)
                self.__draw_grid_lines()
                """
                self.screen.blit(gameover_surface, gameover_rect.topleft)
                pygame.display.update(self.playing_rect)
                pygame.time.wait(speed)
        for row in range(0, rows):
            for col in range(columns - 1, -1, -1):
                # """
                self.grid[row][col] = BACKGROUND_COLOR
                self.draw_board()
                """
                self.draw_square(row, col, BACKGROUND_COLOR, self.__get_top_left)
                self.__draw_grid_lines()
                """
                self.screen.blit(gameover_surface, gameover_rect.topleft)
                pygame.display.update(self.playing_rect)
                pygame.time.wait(speed)

    def set_gravity(self):
        self.gravity_timer = pygame.time.set_timer(GRAVITY, self.falling_interval)

    def new_game(self):
        self.__create_grid()
        self.score = 0
        self.lines_cleared = 0
        self.active_piece = TetrisPiece()
        self.show_next_piece()
        self.show_score()
        self.spawn_piece(self.active_piece)
        self.draw_board()
        self.level = 1
        self.show_level()
        self.falling_interval = self.falling_intervals[self.level]
        self.set_gravity()
        self.show_list(["Enter:", "Pause Game", "", "Esc: ", "End Game"], self.instructions_rect)
        game_paused = False
        game_over = False

        while 1:
            eventos = pygame.event.get()

            for event in eventos:
                self.keyboard_events.set_events(eventos)

                if not game_paused:
                    if event.type == GRAVITY:
                        down = (0, 1)
                        if not self.move_piece(down):
                            game_over = True
                        self.draw_board()

                    if event.type == GAME_TICK:
                        speed = self.keyboard_events.get_direction()
                        if speed != (0, 0):
                            self.move_piece(speed)
                            self.draw_board()

                    if event.type == KEYPRESSED:
                        speed = self.keyboard_events.get_direction()
                        if not self.move_piece(speed):
                            game_over = True
                        self.draw_board()

                if event.type == STARTKEY:
                     game_paused = not game_paused

                if event.type == ESCKEY:
                     game_over = True

            if game_over:
                self.game_over_screen()
                break

    def game_over_screen(self):
        if self.score > self.hiscore:
            self.hiscore = self.score
            self.show_hiscore()

        self.game_over_animation()
        self.draw_start_screen()

    def draw_board(self):
        # self.screen.fill(BLACK)
        self.__draw_grid()
        self.__draw_grid_lines()
        pygame.display.update(self.playing_rect)

    def hiscore_txt_path(self):
        return f'{os.getenv("localappdata")}\\tetris_hiscore.txt'

    @property
    def hiscore(self):
        hiscore_txt_path = self.hiscore_txt_path()
        if os.path.isfile(hiscore_txt_path):
            with open(hiscore_txt_path, "r") as hiscore_txt:
                hiscore = hiscore_txt.read()
            return int(hiscore)
        return 0

    @hiscore.setter
    def hiscore(self, value):
        hiscore_txt_path = self.hiscore_txt_path()
        with open(hiscore_txt_path, "w+") as hiscore_txt:
            hiscore_txt.write(str(int(value)))


class KeyboardEvents:
    def __init__(self, block_length=40):
        self.block_length = block_length
        self.up_key = False
        self.down_key = False
        self.left_key = False
        self.right_key = False
        self.space_key = False
        self.key_pressed_event = pygame.event.Event(KEYPRESSED)
        self.start_key_pressed_event = pygame.event.Event(STARTKEY)
        self.esc_key_pressed_event = pygame.event.Event(ESCKEY)

    def get_direction(self):
        x = 0
        y = 0
        speed = 1
        if self.down_key:
            y = 1
        if self.up_key:
            self.up_key = False
            y = -1
        if self.space_key:
            self.space_key = False
            y = 20
        if self.left_key:
            x += -speed
        if self.right_key:
            x += speed
        if (x, y) != (0, 0):
            pygame.time.set_timer(GAME_TICK, 120)
        else:
            pygame.time.set_timer(GAME_TICK, 0)
        return x, y

    def set_events(self, eventos):
        for event in eventos:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.event.post(self.start_key_pressed_event)
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(self.esc_key_pressed_event)
                if event.key == pygame.K_w:
                    self.up_key = True
                    pygame.event.post(self.key_pressed_event)
                if event.key == pygame.K_a:
                    self.left_key = True
                    self.right_key = False
                    pygame.event.post(self.key_pressed_event)
                if event.key == pygame.K_s:
                    self.down_key = True
                    pygame.event.post(self.key_pressed_event)
                if event.key == pygame.K_d:
                    self.right_key = True
                    self.left_key = False
                    pygame.event.post(self.key_pressed_event)
                if event.key == pygame.K_SPACE:
                    self.space_key = True
                    pygame.event.post(self.key_pressed_event)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.left_key = False
                if event.key == pygame.K_s:
                    self.down_key = False
                if event.key == pygame.K_d:
                    self.right_key = False
