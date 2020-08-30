from queue import Queue
from enum import Enum


class FacingDirection(Enum):
    up = 1
    left = 2
    down = 3
    right = 4


class Snake:

    def __init__(self, x_upper_bound, y_upper_bound, color='green', x_spawn_position=0, y_spawn_position=0,
                 facing_direction=FacingDirection.right, snake_length=3):

        self.__direction = facing_direction
        self.__x_head_current_position = x_spawn_position
        self.__y_head_current_position = y_spawn_position
        self.__color = color
        self.__initial_length = snake_length
        self.__queueSnake = Queue()
        self.__buffer_direction = facing_direction
        self.__x_upper_bound = x_upper_bound
        self.__y_upper_bound = y_upper_bound

    def change_direction(self, direction):
        if direction == FacingDirection.down:
            can_turn = self.__direction != FacingDirection.up
        elif direction == FacingDirection.up:
            can_turn = self.__direction != FacingDirection.down
        elif direction == FacingDirection.left:
            can_turn = self.__direction != FacingDirection.right
        elif direction == FacingDirection.right:
            can_turn = self.__direction != FacingDirection.left

        if can_turn:
            self.__buffer_direction = direction

    """
    def check_collision(self, head):
    if head in self.__queueSnake:
    return True
    """

    def __change_direction(self):
        if self.__buffer_direction == FacingDirection.down:
            can_turn = self.__direction != FacingDirection.up
        elif self.__buffer_direction == FacingDirection.up:
            can_turn = self.__direction != FacingDirection.down
        elif self.__buffer_direction == FacingDirection.left:
            can_turn = self.__direction != FacingDirection.right
        elif self.__buffer_direction == FacingDirection.right:
            can_turn = self.__direction != FacingDirection.left

        if can_turn:
            self.__direction = self.__buffer_direction

    def move(self):
        self.__change_direction()

        if self.__direction == FacingDirection.up:
            self.__y_head_current_position -= 1
        elif self.__direction == FacingDirection.down:
            self.__y_head_current_position += 1
        elif self.__direction == FacingDirection.left:
            self.__x_head_current_position -= 1
        elif self.__direction == FacingDirection.right:
            self.__x_head_current_position += 1

        if self.__x_head_current_position > self.__x_upper_bound - 1:
            self.__x_head_current_position = 0
        elif self.__x_head_current_position < 0:
            self.__x_head_current_position = self.__x_upper_bound - 1

        if self.__y_head_current_position > self.__y_upper_bound - 1:
            self.__y_head_current_position = 0
        elif self.__y_head_current_position < 0:
            self.__y_head_current_position = self.__y_upper_bound - 1

    def add_to_queue(self, cell):
        self.__queueSnake.put(cell)

    def get_tail(self):
        return self.__queueSnake.get()

    @property
    def get_initial_length(self):
        return self.__initial_length

    @property
    def get_color(self):
        return self.__color

    @property
    def head_position(self):
        return self.__x_head_current_position, self.__y_head_current_position

