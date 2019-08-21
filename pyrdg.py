import numpy
import random
import sys

# 1 = Yellow
# 2 = Green
# 3 = Blue
# 4 = Red
# 5 = Purple


class Die():

    def __init__(self):
        self.value = ''
        self.locked = False

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
                self.lock()

    def lock(self):
        self.locked = True

    def unlock(self):
        if self.value != 'R':
            self.locked = False

    def is_locked(self):
        return self.locked

    def reset(self):
        self.__init__()


class Player():

    def __init__(self, turn_order, color):
        self.color = color
        self.score = 10 + turn_order

    # def get_color():
    #     return self.color


class RaTrack():

    def __init__(self, num_players):
        self.END = 13

        if num_players == 4:
            self.start_position = 0
        elif num_players == 3:
            self.start_position = 3
        else:
            self.start_position = 6
        self.position = self.start_position

    def increment(self, steps=1):
        self.position += steps

    def check_end(self):
        return self.position >= self.END

    def print_track(self):
        for x in range(self.END):
            if x == self.start_position:
                print('*', end='')
            else:
                print(str(x)[-1], end='')
        print()
        for x in range(self.END):
            if x == self.position:
                print('X', end='')
            else:
                print('.', end='')
        print()


class Board():

    def __init__(self, num_players):
        self.num_players = num_players
        self.pharaoh_track = self.create_pharaoh_track()
        self.nile_track = self.create_nile_track()
        self.nile_flood = self.create_nile_flood()
        self.civilization_track = self.create_civilization_track()
        self.monument_area = self.create_monument_area()
        self.ra_track = RaTrack(self.num_players)
        self.PHARAOH_TRACK_MAX = 13
        self.NILE_TRACK_MAX = 13

    # CREATE THE BOARD AREAS

    def create_pharaoh_track(self):
        pharaoh_track = [0] * self.num_players
        return pharaoh_track

    def create_nile_track(self):
        # Each player: [ Distance on Nile Track, Number of Flood Cubes ]
        nile_track = [x[:] for x in [[0] * 2] * self.num_players]
        return nile_track

    def create_nile_flood(self):
        nile_flood = [0] * self.num_players
        return nile_flood

    def create_civilization_track(self):
        civilization_track = numpy.zeros((self.num_players, NUM_DICE))
        return civilization_track

    def create_monument_area(self):
        monument_area = numpy.zeros((NUM_DICE, 8))
        return monument_area

    def is_valid_monument_location(self, monument_area, row, col):
        return monument_area[row][col] == 0

    def print_board(self):
        print("Ra Track")
        self.ra_track.print_track()
        print()

        print("Pharaoh Track")
        # print(self.pharaoh_track)
        print('   ', end='')
        for x in range(self.PHARAOH_TRACK_MAX+1):
            print(str(x)[-1], end='')
        print()
        for player in range(self.num_players):
            print('P' + str(player) + ' ', end='')
            for x in range(self.PHARAOH_TRACK_MAX+1):
                if x == self.pharaoh_track[player]:
                    print('X', end='')
                else:
                    print('.', end='')
            print()
        print()

        print("Nile Track")
        # print(self.nile_track)
        print('   ', end='')
        for x in range(self.NILE_TRACK_MAX+1):
            print(str(x)[-1], end='')
        print()
        for player in range(self.num_players):
            print('P' + str(player) + ' ', end='')
            for x in range(self.NILE_TRACK_MAX+1):
                if x == self.nile_track[player][0]:
                    print(str(self.nile_track[player][1]), end='')
                else:
                    print('.', end='')
            print()

        print()

        print("Civ Track")
        print(self.civilization_track)
        print()

        print("Monument Area")
        print(self.monument_area)
        print()


def print_dice(dice):
    NUM_DICE = len(dice)
    for x in range(NUM_DICE):
        print(str(x) + ' ', end='')
    print()

    for x in range(NUM_DICE):
        print(dice[x].value + ' ', end='')
    print()

    for x in range(NUM_DICE):
        if dice[x].is_locked():
            print('*', end='')
        else:
            print(' ', end='')
        print(' ', end='')
    print()


def turn_menu():
    print()
    print("Options:")
    print("L to lock dice")
    print("U to unlock dice")
    print("R to roll again")
    print("S to stop")
    print()
    return str(input("What would you like to do? ")).upper()


# game_over = False
num_players = 2
MAX_ROLLS = 3
MAX_ERAS = 3
NUM_DICE = 5
dice = [None] * NUM_DICE

board = Board(num_players)

player = []
player.append(Player(0, 'blue'))
player.append(Player(1, 'red'))


# Create dice
for x in range(NUM_DICE):
    dice[x] = Die()

player_turn = 0
era = 1

while era <= MAX_ERAS:

    # board.pharaoh_track[0] = 5  # TESTING
    # board.nile_track[0][0] = 5  # TESTING
    # board.nile_track[1][0] = 2  # TESTING
    # board.nile_track[1][1] = 1  # TESTING

    roll = 1
    previous_roll = 0
    while roll <= MAX_ROLLS:
        print()
        print('-'*80)
        print("Era: " + str(era) + " | Player: " + str(player_turn) + " | Roll: " + str(roll) + " | Score: " + str(player[player_turn].score))
        print('-'*80)
        board.print_board()

        # ROLL THE DICE
        if roll != previous_roll:
            previous_roll = roll
            for x in range(NUM_DICE):
                dice[x].roll()

        print_dice(dice)

        # Choose dice to lock, or stop
        selection = turn_menu()

        if selection[0] == 'L':
            dice_to_lock = input("Which dice to lock? ")
            lock_list = [int(s) for s in dice_to_lock.split(',')]
            for x in range(NUM_DICE):
                if x in lock_list:
                    print('Locking ' + str(x))
                    dice[x].lock()

        elif selection[0] == 'U':
            dice_to_unlock = input("Which dice to unlock? ")
            unlock_list = [int(s) for s in dice_to_unlock.split(',')]
            for x in range(NUM_DICE):
                if x in unlock_list:
                    print('Unlocking ' + str(x))
                    dice[x].unlock()

        elif selection[0] == 'R':
            # Next roll
            roll += 1
        elif selection[0] == 'S':
            # If stop, set roll to 4
            roll = 4
        else:
            print("Invalid option")
            sys.exit

    # "Score" this turn
    for x in range(NUM_DICE):
        if dice[x].value == 'P':
            board.pharaoh_track[player_turn] += 1
        elif dice[x].value == 'N':
            board.nile_track[player_turn][0] += 1
        elif dice[x].value == 'R':
            board.ra_track.increment()

    # Next player's turn
    if player_turn == num_players-1:
        player_turn = 0
    else:
        player_turn += 1

    # RESET THE DICE
    for x in range(NUM_DICE):
        dice[x].reset()

    # END IT NOW
    # era = 4
    # if board.ra_track.check_end():

    #     if era == 3:
    #         # do final scoring
    #         pass

    #     era += 1
