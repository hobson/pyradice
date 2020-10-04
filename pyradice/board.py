import pygame
from .constants import BOARD_IMAGE

class Board:
    def __init__(self, win):
        self.board = []
        self.win = win
        self.draw_board()

    def draw_board(self):
        self.win.blit(BOARD_IMAGE, (0,0))
