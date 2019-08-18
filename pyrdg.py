import numpy
import random

# 1 = Yellow
# 2 = Green
# 3 = Blue
# 4 = Red
# 5 = Purple


class Die():

    def __init__(self):
        self.value = ''
        self.lock = False

    def roll(self):
        if not self.is_locked():
            roll = random.randint(1, 6)
            if roll == 1:
                self.value = 'P'  # Pharaoh
            elif roll == 2:
                self.value = 'N'  # Nile
            elif roll == 3:
                self.value = 'C'  # Civilization
            elif roll == 4:
                self.value = 'M'  # Monument
            elif roll == 5:
                self.value = 'A'  # Ankh
            else:
                self.value = 'R'  # Ra

    def lock(self):
        self.lock = True

    def unlock(self):
        self.lock = False

    def is_locked(self):
        return self.lock

    def reset(self):
        self.__init__


class Player():

    def __init__(self, color):
        self.color = color
        self.score = 0

    # def get_color():
    #     return self.color


class RaTrack():

    def __init__(self, num_players):
        self.end = 13

        if num_players == 4:
            self.position = 1
        elif num_players == 3:
            self.position = 4
        else:
            self.position = 7

    def increment(self, steps=1):
        self.position += steps

    def check_end(self):
        return self.position >= self.end

    def print_track(self):
        for x in range(self.end):
            if x == self.position:
                print('X', end='')
            else:
                print('.', end='')
        print()


class Board():

    def __init__(self, num_players):
        self.pharaoh_track = self.create_pharaoh_track(num_players)
        self.nile_track = self.create_nile_track(num_players)
        self.civilization_track = self.create_civilization_track(num_players)
        self.monument_area = self.create_monument_area()
        self.ra_track = RaTrack(num_players)

    # CREATE THE BOARD AREAS

    def create_pharaoh_track(self, num_players):
        pharaoh_track = numpy.zeros((num_players, 13))
        return pharaoh_track

    def create_nile_track(self, num_players):
        nile_track = numpy.zeros((num_players, 13))
        return nile_track

    def create_civilization_track(self, num_players):
        civilization_track = numpy.zeros((num_players, 5))
        return civilization_track

    def create_monument_area(self):
        monument_area = numpy.zeros((5, 8))
        return monument_area

    def is_valid_monument_location(self, monument_area, row, col):
        return monument_area[row][col] == 0

    def print_board(self):
        print("Ra Track")
        self.ra_track.print_track()
        print()

        print("Pharaoh Track")
        print(self.pharaoh_track)
        print()

        print("Nile Track")
        print(self.nile_track)
        print()

        print("Civ Track")
        print(self.civilization_track)
        print()

        print("Monument Area")
        print(self.monument_area)
        print()


game_over = False
num_players = 2
MAX_ROLLS = 3
MAX_ERAS = 3
NUM_DICE = 5
dice = [None] * 5

board = Board(num_players)

player = []
player.append(Player('blue'))
player.append(Player('red'))


# Create dice
for x in range(NUM_DICE):
    dice[x] = Die()

turn = 1
era = 1

while era <= MAX_ERAS:

    board.print_board()

    roll = 1
    while roll <= MAX_ROLLS:
        print("Era is " + str(era))
        print("Roll is " + str(roll))
        # ROLL THE DICE
        for x in range(NUM_DICE):
            dice[x].roll()

        # print the dice
        # for x in range(NUM_DICE):
        #     print(dice[x].value)
        # Choose dice to lock, or stop

        # If stop, set roll to 4

        # Next roll
        roll += 1

    # "Score" this turn

    # Next player's turn
    if turn == num_players:
        turn = 0
    else:
        turn += 1

    # RESET THE DICE
    for x in range(NUM_DICE):
        dice[x].reset()

    # END IT NOW
    era = 4
    # if board.ra_track.check_end():

    #     if era == 3:
    #         # do final scoring
    #         pass

    #     era += 1
