#!/usr/bin/env python
# coding=utf-8
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

"""
TODO:
    SPEED depends on size
    no boundary
    title screen to choose this
"""

pygame.init()
font = pygame.font.SysFont('arial', 25)


# reset
#reward
# play (action) -> direction
#game iteration
#is_iteration


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

############## CONSTANTS ###############
BLOCK_SIZE = 20
SPEED = 400 # maybe can depend on size of the snake
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

class SnakeGameIA:
    def __init__(self, weidth=640, height=480):
        self.weidth = weidth
        self.height = height

        #init display

        self.display = pygame.display.set_mode((self.weidth, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()


        
    def reset(self):
        #init game state
        self.direction = Direction.RIGHT

        #strat in the middle
        self.head = Point(self.weidth/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2 * BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0


    def play_step(self, action):
        self.frame_iteration += 1
        # 1 collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        #2 move
        self._move(action)
        self.snake.insert(0, self.head)# ahead of one block

        #Game over ?
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        #4 Place new food
        if self.head == self.food:
            self.score += 1 
            reward = 10
            self._place_food() 
        else:
            self.snake.pop() # remove if no block eaten

        #5 update ui
        self._update_ui()
        #SPEED = (len(self.snake) - 1) * 1.5
        self.clock.tick(SPEED)

        #6 go and score
        return reward, game_over, self.score

    def _place_food(self):
        x = random.randint(0, (self.weidth-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()


    def _update_ui(self):
        self.display.fill(BLACK)
        for p in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(p.x, p.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(p.x + 4, p.y + 4, 2 * BLOCK_SIZE//3, 2 * BLOCK_SIZE//3))
 
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE//2, BLOCK_SIZE//2))

        text = font.render("Score:" + str(self.score), True, WHITE)
        self.display.blit(text, [0,0])
        pygame.display.flip()#update the changes

    def _move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT,Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            new_dir = clock_wise[(idx + 1)%4]
        else:
            new_dir = clock_wise[(idx - 1)%4]
        
        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if self.direction == Direction.UP:
            y -= BLOCK_SIZE
        if self.direction == Direction.DOWN:
            y += BLOCK_SIZE


        self.head = Point(x, y)

    def is_collision(self, pt=None):
        """
        check if hit boundary or itself
        """
        if pt is None:
            pt = self.head
        if pt.x > self.weidth - BLOCK_SIZE or pt.x < 0 or pt.y > self.height - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        return False

