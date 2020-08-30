from tkinter import *
from tkinter import messagebox

from random import randint
from ClsSnake.Snake import Snake, FacingDirection
from queue import Queue


class TkinterFigure:

    def __init__(self, tkinter_id, x, y, cell_type):
        self.__id = tkinter_id
        self.__x = x
        self.__y = y
        self.__cell_type = cell_type

    @property
    def position(self):
        return self.__x, self.__y

    @property
    def id(self):
        return self.__id

    @property
    def cell_type(self):
        return self.__cell_type

    def __str__(self):
        return f'{self.__cell_type} ID: {self.__id} X: {self.__x} Y: {self.__y}'

    def __eq__(self, other):
        x, y = other.position

        if self.__x == x and self.__y == y:
            return True
        return False


class SnakePlayground:

    def __init__(self, height=800, width=800, cell_side_length=50, padding=5, tick_ms=300, bg='grey'):
        self.__FOOD_COLOR = 'red'
        self.__SNAKE_COLOR = 'green'

        self.__root = Tk()
        self.__root.title("Snake :)")

        self.__root.iconbitmap("D:\Eu\Piton\Proyectitos\SnakePythonXd\ClsPlayGround\snake_icon.ico")
        self.__playAreaHeight = height
        self.__playAreaWidth = width

        self.__gridCellLength = cell_side_length
        self.__padding = padding
        self.__square_side = self.__gridCellLength - 2 * self.__padding

        self.__xUpperBound = self.__playAreaHeight / self.__gridCellLength
        self.__yUpperBound = self.__playAreaWidth / self.__gridCellLength

        self.__score = 0
        self.__snake = Snake(self.__xUpperBound, self.__yUpperBound, snake_length=5)
        self.__snake_list = []

        self.__xLowerBound = 0
        self.__yLowerBound = 0

        self.__tick_ms = tick_ms
        self.__current_speed = 0
        self.__canvas = Canvas(self.__root, height=self.__playAreaHeight, width=self.__playAreaWidth, bg=bg)
        self.__canvas.pack()
        self.__create_menu()

    def __create_binds(self):
        self.__root.bind('<w>', self.__key)
        self.__root.bind('<a>', self.__key)
        self.__root.bind('<s>', self.__key)
        self.__root.bind('<d>', self.__key)

    def __remove_binds(self):
        self.__root.unbind('<w>')
        self.__root.unbind('<a>')
        self.__root.unbind('<s>')
        self.__root.unbind('<d>')

    def __key(self, event):
        if repr(event.char) == "'w'":
            self.__snake.change_direction(FacingDirection.up)
        elif repr(event.char) == "'a'":
            self.__snake.change_direction(FacingDirection.left)
        elif repr(event.char) == "'s'":
            self.__snake.change_direction(FacingDirection.down)
        elif repr(event.char) == "'d'":
            self.__snake.change_direction(FacingDirection.right)

    def create_game(self):
        self.__show_menu()
        self.__root.mainloop()

    def __show_demo(self):
        self.__demo_canvas = Canvas(self.__root, height=self.__playAreaHeight, width=self.__playAreaWidth, bg=bg)
        self.__demo_snake = Snake(self.__xUpperBound, self.__yUpperBound, snake_length=5)

    def __start_new_game(self):
        self.__create_binds()
        self.__hide_menu()
        self.__score = 0
        self.__snake = Snake(self.__xUpperBound, self.__yUpperBound, snake_length=5)
        self.__snake_list = []

        self.__create_food()
        self.__spawn_snake()

        self.__current_speed = self.__tick_ms

        self.__root.after(self.__tick_ms, self.__move)

    def __move(self):
        self.__snake.move()


        try:
            snake_piece = self.__draw_snake()
            if snake_piece == self.__food:
                # if the snake eats the food it creates a new one
                self.__canvas.delete(self.__food.id)
                self.__create_food()
                self.__score += 1
                if self.__current_speed > 125 and self.__score % 5 == 0:
                    self.__current_speed = int(self.__current_speed * 0.8)

            else:
                # else move and delete the tail
                tail = self.__snake.get_tail()
                self.__snake_list.remove(tail)
                self.__canvas.delete(tail.id)
            self.__root.after(self.__current_speed, self.__move)

        except GameOver:
            messagebox.showinfo("Game Over!", f'Game is over :( \n Your score is {self.__score}')
            self.__remove_binds()
            self.__canvas.delete(ALL)
            self.__snake_list.clear()
            self.__show_menu()

    def __create_menu(self):
        self.__start_button = Button(self.__root, text="Play", command=self.__start_new_game)
        self.__quit_button = Button(self.__root, text="Quit", command=self.__quit)

    def __quit(self):
        self.__root.quit()

    def __show_menu(self):
        self.__start_button.pack()
        self.__quit_button.pack()

    def __hide_menu(self):
        self.__start_button.pack_forget()
        self.__quit_button.pack_forget()

    def __create_food(self):

        food_spawn_position_x = randint(self.__xLowerBound, self.__xUpperBound - 1)
        food_spawn_position_y = randint(self.__yLowerBound, self.__yUpperBound - 1)
        check_cell = TkinterFigure(-1, food_spawn_position_x, food_spawn_position_y, "test")

        while check_cell in self.__snake_list:
            food_spawn_position_x = randint(self.__xLowerBound, self.__xUpperBound - 1)
            food_spawn_position_y = randint(self.__yLowerBound, self.__yUpperBound - 1)
            check_cell = TkinterFigure(-1, food_spawn_position_x, food_spawn_position_y, "test")

        cell_created = self.create_square(food_spawn_position_x, food_spawn_position_y, self.__FOOD_COLOR)
        self.__food = TkinterFigure(cell_created, food_spawn_position_x, food_spawn_position_y, "food")

    def __get_coordinates(self, x, y):
        x_coordinate = x * self.__gridCellLength + self.__padding
        y_coordinate = y * self.__gridCellLength + self.__padding

        return x_coordinate, y_coordinate

    def __spawn_snake(self):
        initial_length = self.__snake.get_initial_length

        for i in range(0, initial_length):
            self.__snake.move()
            self.__draw_snake()

    def __draw_snake(self):
        x, y = self.__snake.head_position
        color = self.__snake.get_color
        grid_cell = self.create_square(x, y, color)
        snake_piece = TkinterFigure(grid_cell, x, y, "snake")

        # add the piece of the snake to the end of the queue in snake object
        self.__snake.add_to_queue(snake_piece)
        peek_queue = self.__snake

        if snake_piece in self.__snake_list:
            self.__canvas.delete(snake_piece.id)
            raise GameOver("Game Over :c")

        # adds the piece of the snake to a list containing all the pieces
        self.__snake_list.append(snake_piece)

        return snake_piece

    def create_square(self, x, y, color):
        x_coordinate, y_coordinate = self.__get_coordinates(x, y)

        grid_cell = self.__canvas.create_rectangle(x_coordinate, y_coordinate, x_coordinate + self.__square_side,
                                                   y_coordinate + self.__square_side, fill=color, outline="")
        return grid_cell


class GameOver(Exception):
    pass
