#!/usr/bin/env python
# coding=utf-8
import pygame
import random

pygame.init()

class SnakeGame:
    def __init__(self, weidth=640, height=480):
        self.weidth = weidth
        self.height = height

        #init display

        self.display = pygame.display.set_mode((self.weidth, self.height))
        pygame.display.set_caption('Snake')
        #init game state

    def play_step(self):
        pass


if __name__ == '__main__':
    game = SnakeGame()

    while True:
        game.play_step()

        #break if game over


    pygame.quit()
