from PIL import Image
a=Image.open("istockphoto-455302535-612x612.jpg")
a.show()
class GamePlayer:
    # Encapsulates a player properties

    def __init__(self, _id):
        self._id = _id
        self.rank = -1
        self.position = 0
     # Start at position 0

    def set_position(self, pos):
        self.position = pos

    def set_rank(self, rank):
        self.rank = rank

    def get_pos(self):
        return self.position

    def get_rank(self):
        return self.rank


class MovingEntity:
    # we have  create  the  moving entity i.e. snake and  ladder by this class

    def __init__(self, end_pos=None):
        self.end_pos = end_pos
        self.desc = None

    def set_description(self, desc):
        self.desc = desc

    def get_end_pos(self):
        if self.end_pos is None:
            raise Exception("no_end_position_defined")
        return self.end_pos


class Snake(MovingEntity):
    # Snake entity

    def __init__(self, end_pos=None):
        super(Snake, self).__init__(end_pos)
        self.desc = "Bit by Snake"


class Ladder(MovingEntity):
    # Ladder entity

    def __init__(self, end_pos=None):
        super(Ladder, self).__init__(end_pos)
        self.desc = "Climbed Ladder"


class Board:
    # Define board with size and moving entities
    # self.board Uses the concept of Incapsulation
    def __init__(self, size):
        self.size = size
        self.board = {}
    def get_size(self):
        return self.size
    # Here sert_moving_entity used the concept of dependency injection
    def set_moving_entity(self, pos, moving_entity):
        self.board[pos] = moving_entity

    def get_next_pos(self, player_pos):
        if player_pos not in self.board:
            return player_pos
        # If Player is bit by snake or has climb a ladder by calling desc function of moving entity which is stored as a value in the dictionary board
        print(f'{self.board[player_pos].desc} at {player_pos}')
        return self.board[player_pos].get_end_pos()

    def at_last_pos(self, pos):
        if pos == self.size:
            return True
        return False


class Dice:
    # adding flexibility to the code by make it to work on dice of any  number
    def __init__(self, sides):
        self.sides = sides

    def roll(self):
        import random
        ans = random.randrange(1, self.sides + 1)
        return ans


class Game:
    def __init__(self):
        self.board = None
        self.dice = None
        self.players = []
        self.turn = 0
        self.winner = None
        self.last_rank = 0
        self.consecutive_six = 0
    # Type Hinting board:Board
    def initialize_game(self, board: Board, dice_sides, num_players):
        self.board = board
        self.dice = Dice(dice_sides)
        self.players = [GamePlayer(i) for i in range(num_players)]

    def can_play(self):
        return self.winner is None

    def current_player(self):
        return self.players[self.turn]

    def move_player(self, curr_player, next_pos):
        curr_player.set_position(next_pos)
        if self.board.at_last_pos(curr_player.get_pos()):
            # curr_player.set_rank(self.last_rank + 1)
            self.winner=curr_player

    def can_move(self, curr_player, to_move_pos):
        if to_move_pos <= self.board.get_size() and curr_player.get_rank() == -1:
            return True
        return False

    def change_turn(self, dice_result):
        self.consecutive_six = 0 if dice_result != 6 else self.consecutive_six + 1
        if dice_result != 6 or self.consecutive_six == 3:
            if self.consecutive_six == 3:
                print("Changing turn due to 3 consecutive sixes")
            # Note can not directly call _player as it is rank based not based on result of dice 
            self.turn = (self.turn + 1) % len(self.players)
        else:
            print(f"One more turn for player {self.turn+1} after rolling 6")

    def play(self):
        while self.can_play():
            curr_player = self.current_player()
            # self.turn+1 as it is index pf players[] self.turn=0 means turn of player 1
            input(f"Player {self.turn+1}, Press enter to roll the dice")
            dice_result = self.dice.roll()
            print(f'dice_result: {dice_result}')
            next_pos = self.board.get_next_pos(curr_player.get_pos() + dice_result)
            if self.can_move(curr_player, next_pos):
                self.move_player(curr_player, next_pos)
            self.change_turn(dice_result)
            self.print_game_state()
        self.print_game_result()
            

    def print_game_state(self):
        print('-------------game state-------------')
        for ix, _p in enumerate(self.players):
            print(f'Player: {ix+1} is at pos {_p.get_pos()}')
        # Alternative form of using for loop when we require both index and value at that index
        # for ix in range(len(self.players)):
        #     player = self.players[ix]
        #     print(f'Player: {ix+1} is at pos {player.get_pos()}')

        print('-------------game state-------------\n\n')

    def print_game_result(self):
        print(f'Player {self.winner._id +1} has won the game!')
        print("The Leaderboard is as follow:")
         # Sort players based on their positions in descending order
        leaderboard = sorted(self.players, key=lambda x: x.get_pos(), reverse=True)

        # Assign ranks based on positions
        rank = 1
        prev_pos = None
        for player in leaderboard:
            if player.get_pos() != prev_pos:
                print(f"{rank}. Player {player._id+1}")
            prev_pos = player.get_pos()
            rank += 1



class BoardSetup:
    @staticmethod
    def setup():
        board = Board(100)

        snakes = {
            17: 7,
            62: 19,
            87: 24,
            54: 34,
            64: 60,
            93: 73,
            95: 75,
            98: 79
        }
        for start, end in snakes.items():
            board.set_moving_entity(start, Snake(end))

        ladders = {
            1: 38,
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            51: 67,
            71: 91,
            80: 100
        }
        for start, end in ladders.items():
            board.set_moving_entity(start, Ladder(end))

        return board


def get_num_players():
    while True:
        try:
            num_players = int(input("Enter the number of players: "))
            if num_players > 0:
                return num_players
            else:
                print("Number of players must be greater than 0.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def run():
    num_players = get_num_players()
    board = BoardSetup.setup()
    game = Game()
    game.initialize_game(board, 6, num_players)
    game.play()


run()