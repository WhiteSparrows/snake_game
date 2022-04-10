#!/usr/bin/env python
# coding=utf-8
import pygame
import random
from enum import Enum
from collections import namedtuple

"""
TODO:
    SPEED depends on size
    no boundary
    title screen to choose this
"""

pygame.init()
font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

############## CONSTANTS ###############
BLOCK_SIZE = 20
SPEED = 10 # maybe can depend on size of the snake
# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)

class SnakeGame:
    def __init__(self, weidth=640, height=480):
        self.weidth = weidth
        self.height = height

        #init display

        self.display = pygame.display.set_mode((self.weidth, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()


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
        

    def play_step(self):
        # 1 collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    if self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    if self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    if self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                break
        
        #2 move
        self._move(self.direction)
        self.snake.insert(0, self.head)# ahead of one block

        #Game over ?
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, score
        
        #4 Place new food
        if self.head == self.food:
            self.score += 1 
            self._place_food() 
        else:
            self.snake.pop() # remove if no block eaten

        #5 update ui
        self._update_ui()
        SPEED = (len(self.snake) - 1) * 1.5
        self.clock.tick(SPEED)

        #6 go and score
        game_over = False
        return game_over, self.score

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

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        if direction == Direction.LEFT:
            x -= BLOCK_SIZE
        if direction == Direction.UP:
            y -= BLOCK_SIZE
        if direction == Direction.DOWN:
            y += BLOCK_SIZE


        self.head = Point(x, y)

    def _is_collision(self):
        """
        check if hit boundary or itself
        """
        if self.head.x > self.weidth - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        return False

if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game_over, score = game.play_step()

        if game_over:
            break
    print(f"The final score is {score}")

        #break if game over


    pygame.quit()
