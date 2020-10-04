import pygame
import os

# GAME_WIDTH, GAME_HEIGHT = 2826, 2084
GAME_WIDTH, GAME_HEIGHT = int(2826/2), int(2084/2)

__BOARD_IMAGE_FILE = os.path.join(os.path.dirname(__file__), 'assets/ra_dice_board_original.jpg')    # Get the relative path of the image within the module directory as a "private" variable
BOARD_IMAGE = pygame.transform.scale(pygame.image.load(__BOARD_IMAGE_FILE), (GAME_WIDTH, GAME_HEIGHT))
