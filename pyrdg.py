import numpy
import random


# CREATE THE BOARD AREAS
def create_pharaoh_track(num_players):
    pharaoh_track = numpy.zeros((num_players, 13))
    return pharaoh_track


def create_nile_track(num_players):
    nile_track = numpy.zeros((num_players, 13))
    return nile_track


def create_civilization_track(num_players):
    civilization_track = numpy.zeros((num_players, 5))
    return civilization_track


def create_monument_area():

    monument_area = numpy.zeros((5, 8))
    return monument_area


def is_valid_monument_location(monument_area, row, col):
    return monument_area[row][col] == 0


def roll_die():
    return randomint(1, 6)


class Player():

    def __init__(self, color):
        self.color = color
        self.score = 0

    # def get_color():
    #     return self.color


class RaTrack():

    def __init__(self, num_players):
        if num_players == 4:
            self.position = 1
        elif num_players == 3:
            self.position = 4
        else:
            self.position = 7


game_over = False
num_players = 2

players = []
players.append(Player('blue'))
players.append(Player('red'))

pharaoh_track = create_pharaoh_track(num_players)
nile_track = create_nile_track(num_players)
civilization_track = create_civilization_track(num_players)
monument_area = create_monument_area()
ra_track = RaTrack(num_players)


# while not game_over:
