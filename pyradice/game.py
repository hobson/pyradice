import pygame
from pyradice.board import Board

class  Game:
    def __init__(self, win):
        self.win = win
        self._init()

    def update(self):
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board(self.win)

    def winner(self):
        return self.board.winner()

    # def reset(self):
    #     self._init()
