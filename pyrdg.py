import numpy
import random
import sys

from colorama import init, Fore, Back, Style
import colorama
colorama.init(autoreset=True)    # Colorama


class Die():

    def __init__(self, color):
        self.color = color
        self.fgcolor = colorama.Fore.WHITE
        self.style = colorama.Style.BRIGHT
        self.value = ''
        self.locked = False
        self.available = True
        self.POSSIBLE_DICE_VALUE = ['P', 'N', 'C', 'M', 'A', 'R']  # Pharaoh, Nile, Civilization, Monument, Ankh, Ra

        if self.color == 'yellow':
            self.bgcolor = colorama.Back.YELLOW
        elif self.color == 'green':
            self.bgcolor = colorama.Back.GREEN
        elif self.color == 'blue':
            self.bgcolor = colorama.Back.BLUE
        elif self.color == 'red':
            self.bgcolor = colorama.Back.RED
        elif self.color == 'purple':
            self.bgcolor = colorama.Back.MAGENTA
        else:
            sys.exit('Invalid die color')

    def roll(self):
        if not self.is_locked():
            self.value = self.POSSIBLE_DICE_VALUE[random.randint(0, 5)]
            self.value = 'C'
            if self.value == 'R':
                self.lock()
                self.available = False

    def lock(self):
        self.locked = True

    def unlock(self):
        if self.value != 'R':
            self.locked = False

    def is_locked(self):
        return self.locked

    def use(self):
        self.available = False

    def is_available(self):
        return self.available

    def format(self):
            return self.fgcolor + self.bgcolor + self.style

    def print_colored_value(self):
        print(self.bgcolor + self.fgcolor + self.style + ' ' + self.value + ' ', end='')

    def reset(self):
        self.__init__(self.color)


class Player():

    def __init__(self, turn_order, color):
        self.color = color
        self.score = 10 + turn_order

    # def get_color():
    #     return self.color


class RaTrack():

    def __init__(self, num_players):
        self.END = 13
        self.NUM_PLAYERS = num_players

        if self.NUM_PLAYERS == 4:
            self.start_position = 0
        elif self.NUM_PLAYERS == 3:
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

    def reset(self):
        self.__init__(self.NUM_PLAYERS)


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
        for player in range(self.num_players):
            print('P' + str(player) + ' ', end='')
            for x in range(NUM_DICE):
                print(dice[int(x)].format() + ' ' + str(int(self.civilization_track[player][x])) + ' ', end='')
            print()

        print()

        print("Monument Area")
        print(self.monument_area)
        print()


def print_dice(dice):
    NUM_DICE = len(dice)
    for x in range(NUM_DICE):
        print(' ' + str(x) + '  ', end='')
    print()

    for x in range(NUM_DICE):
        dice[x].print_colored_value()
        print(' ', end='')
    print()

    for x in range(NUM_DICE):
        if dice[x].is_locked():
            print(' * ', end='')
        elif not dice[x].is_available():
            print(' U ', end='')
        else:
            print('   ', end='')
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

# def yes_or_no(question):
#     check = str(input(question + " (Y/N): ")).lower().strip()
#     try:
#         if check[0] == 'y':
#             return True
#         elif check[0] == 'n':
#             return False
#         else:
#             print('Invalid Input')
#             return yes_or_no(question)
#     except Exception as error:
#         print("Please enter valid inputs!")
#         print(error)
#         return yes_or_no(question)


# game_over = False
MAX_ROLLS = 3
MAX_ERAS = 3
NUM_DICE = 5
dice = [None] * NUM_DICE

player = []
player.append(Player(0, 'blue'))
player.append(Player(1, 'red'))
# player.append(Player(2, 'green'))
# player.append(Player(3, 'yellow'))
NUM_PLAYERS = len(player)

board = Board(NUM_PLAYERS)

# Create dice
dice[0] = Die('yellow')
dice[1] = Die('green')
dice[2] = Die('blue')
dice[3] = Die('red')
dice[4] = Die('purple')

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
        print("Era: " + str(era) + " | Player: " + str(player_turn) + " | Roll: " + str(roll) + " | Scores: ", end='')
        for x in range(NUM_PLAYERS):
            print('P' + str(x) + ':' + str(player[x].score) + ' ', end='')
        print()
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
            # If stop, set roll above the max
            roll = MAX_ROLLS + 1
        else:
            print("Invalid option")

    # "Score" this turn
    # Count the dice values
    for value in ['P', 'N', 'C', 'M', 'A', 'R']:
        quantity = sum(1 for d in dice if d.value == value)
        # print(value + ': ' + str(quantity))

    # for x in range(NUM_DICE):
    #     if dice[x].value == 'P':
    #         board.pharaoh_track[player_turn] += 1
    #     elif dice[x].value == 'N':
    #         board.nile_track[player_turn][0] += 1
    #     elif dice[x].value == 'R':
    #         board.ra_track.increment()

    ########## DECIDE FOR PHARAOH TRACK ##########
    while True:
        invalid_response_count = 0
        chosen_values = []
        ptrackdice = list(filter(None, input('Which dice would you like to use on the Pharaoh track? ').split(",")))
        if len(ptrackdice) != 0:
            for x in ptrackdice:
                face_value = dice[int(x)].value
                if face_value not in ['P', 'A']:
                    invalid_response_count += 1
                    print('Invalid response ' + str(x) + ' (' + face_value + '}')
                else:
                    chosen_values.append(dice[int(x)].value)
            # print(chosen_values)
            countp = sum(1 for c in chosen_values if c == 'P')
            if countp == 0:
                print('At least one chosen die must be Pharaoh!')
                invalid_response_count += 1
        if invalid_response_count == 0:
            break

    psum = len(chosen_values)
    for x in ptrackdice:
        dice[int(x)].use()
    board.pharaoh_track[player_turn] = min(board.PHARAOH_TRACK_MAX, board.pharaoh_track[player_turn] + psum)
    ########## END PHARAOH TRACK ##########

    ########## DECIDE FOR NILE FLOOD ##########
    print_dice(dice)

    # if yes_or_no("Would you like to flood?"):
    while True:
        invalid_response_count = 0
        chosen_values = []
        flooddice = list(filter(None, input('Which dice would you like to use to flood? ').split(",")))
        if len(flooddice) != 0:
            for x in flooddice:
                face_value = dice[int(x)].value
                if face_value not in ['N', 'A']:
                    invalid_response_count += 1
                    print('Invalid response ' + str(x) + ' (' + face_value + '}')
                else:
                    chosen_values.append(dice[int(x)].value)
            # print(chosen_values)
            countn = sum(1 for c in chosen_values if c == 'N')
            countf = sum(1 for c in chosen_values if c in ['N','A'])
            if countn == 0:
                print('At least one chosen die must be Nile!')
                invalid_response_count += 1
            if countn != 3:
                print('You must pick only 3 dice when flooding!')
                invalid_response_count += 1
        if invalid_response_count == 0:
            break

    fsum = len(chosen_values)
    if fsum == 3:
        for x in flooddice:
            dice[int(x)].use()
        board.nile_track[player_turn][1] += 1
    ########## END NILE FLOOD ##########

    ########## DECIDE FOR NILE TRACK ##########
    print_dice(dice)
    while True:
        invalid_response_count = 0
        chosen_values = []
        ntrackdice = list(filter(None, input('Which dice would you like to use on the Nile track? ').split(",")))
        if len(ntrackdice) != 0:
            for x in ntrackdice:
                face_value = dice[int(x)].value
                if face_value not in ['N', 'A']:
                    invalid_response_count += 1
                    print('Invalid response ' + str(x) + ' (' + face_value + '}')
                else:
                    chosen_values.append(dice[int(x)].value)
            # print(chosen_values)
            countn = sum(1 for c in chosen_values if c == 'N')
            if countn == 0:
                print('At least one chosen die must be Nile!')
                invalid_response_count += 1
        if invalid_response_count == 0:
            break

    nsum = len(chosen_values)
    for x in ntrackdice:
        dice[int(x)].use()
    board.nile_track[player_turn][0] = min(board.NILE_TRACK_MAX, board.nile_track[player_turn][0] + nsum)
    ########## END NILE TRACK ##########

    ########## DECIDE FOR CIV TRACK ##########
    print_dice(dice)
    while True:
        invalid_response_count = 0
        chosen_values = []
        ctrackdice = list(filter(None, input('Which dice would you like to use on the Civ track? ').split(",")))
        if len(ctrackdice) != 0:
            for x in ctrackdice:
                face_value = dice[int(x)].value
                if face_value not in ['C', 'A']:
                    invalid_response_count += 1
                    print('Invalid response ' + str(x) + ' (' + face_value + '}')
                else:
                    chosen_values.append(dice[int(x)].value)
            # print(chosen_values)
            countc = sum(1 for c in chosen_values if c == 'C')
            countc_all = sum(1 for c in chosen_values if c in ['C','A'])
            if countc == 0:
                print('At least one chosen die must be Civ!')
                invalid_response_count += 1
            if countc_all < 3:
                print('You must pick at least 3 dice when choosing Civs!')
                invalid_response_count += 1
        if invalid_response_count == 0:
            break

    civs_to_place = len(ctrackdice) - 2

    while True:
        invalid_response_count = 0
        chosen_values = []
        c2trackdice = list(filter(None, input('Which ' + str(civs_to_place) + ' civ(s) would you like to place? ').split(",")))
        if len(c2trackdice) != 0:
            for x in c2trackdice:
                face_value = dice[int(x)].value
                if face_value not in ['C']:
                    invalid_response_count += 1
                    print('Invalid response ' + str(x) + ' (' + face_value + '}')
                elif x not in ctrackdice:
                    invalid_response_count += 1
                    print('Invalid response: die ' + str(x) + ' was not in the civ list.')
                elif board.civilization_track[player_turn][int(x)] == 1:
                    invalid_response_count += 1
                    print('You already have a civ in color ' + dice[int(x)].color + '.')
                else:
                    players_in_this_color = 0
                    for p in range(NUM_PLAYERS):
                        if board.civilization_track[p][int(x)] == 1:
                            players_in_this_color += 1
                    if players_in_this_color >= NUM_PLAYERS - 1:
                        invalid_response_count += 1
                        print('There are already the max number (' + str(NUM_PLAYERS - 1) + ') of civs in col0r ' + dice[int(x)].color + '.')
                    else:
                        chosen_values.append(dice[int(x)].value)
            # print(chosen_values)
            if invalid_response_count == 0:
                countc = sum(1 for c in chosen_values if c == 'C')
                if countc < civs_to_place:
                    print('You only chose ' + str(countc) + '/' + str(civs_to_place) + ' dice.')
                    invalid_response_count += 1
                elif countc > civs_to_place:
                    print('Too many! You chose ' + str(countc) + ' dice but are only allowed ' + str(civs_to_place) + '.')
                    invalid_response_count += 1
        if invalid_response_count == 0:
            break

    for x in ctrackdice:
        dice[int(x)].use()
        if x in c2trackdice:
            board.civilization_track[player_turn][int(x)] = 1
    ########## END CIV TRACK ##########

    # Next player's turn
    if player_turn == NUM_PLAYERS-1:
        player_turn = 0
    else:
        player_turn += 1

    # RESET THE DICE
    for x in range(NUM_DICE):
        dice[x].reset()

    # Check for end of Era
    if board.ra_track.check_end():
        board.ra_track.reset()

        # End of era-scoring

        # Swtch to next era
        era += 1
