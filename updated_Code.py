"""
Snake and Ladder Game Implementation

This module contains classes to simulate a simple Snake and Ladder game.

Classes:
- GamePlayer: Encapsulates a player's properties including their position and rank.
- MovingEntity: A base class for defining moving entities such as snakes or ladders.
- Snake: Represents a snake entity on the game board.
- Ladder: Represents a ladder entity on the game board.
- Board: Defines the game board with size and tracks the positions of moving entities.
- Dice: Simulates the rolling of a dice with a given number of sides.
- Game: Orchestrates the gameplay logic including player movements, turns, and game state.

Functions:
- sample_run: Executes a sample run of the game with predefined board configurations and player settings.
"""

class GamePlayer:
    """
    Encapsulates a player's properties in the game.
    
    Attributes:
    - _id: The unique identifier of the player.
    - rank: The rank achieved by the player (-1 if still playing).
    - position: The current position of the player on the board.
    """

    def __init__(self, _id):
        """
        Initialize a GamePlayer object.

        Parameters:
        - _id (int): The unique identifier of the player.
        """
        self._id = _id
        self.rank = -1
        self.position = 1

    def set_position(self, pos):
        """Set the position of the player on the board."""
        self.position = pos

    def set_rank(self, rank):
        """Set the rank achieved by the player."""
        self.rank = rank

    def get_pos(self):
        """Get the current position of the player."""
        return self.position

    def get_rank(self):
        """Get the rank achieved by the player."""
        return self.rank


class MovingEntity:
    """
    Base class for defining moving entities on the game board such as snakes or ladders.

    Attributes:
    - end_pos: The position where the player will be sent after encountering this entity.
    - desc: Description of the moving entity.
    """

    def __init__(self, end_pos=None):
        """
        Initialize a MovingEntity object.

        Parameters:
        - end_pos (int, optional): The position where the player will be sent after encountering this entity.
        """
        self.end_pos = end_pos
        self.desc = None

    def set_description(self, desc):
        """Set the description of the moving entity."""
        self.desc = None

    def get_end_pos(self):
        """Get the position where the player will be sent after encountering this entity."""
        if self.end_pos is None:
            raise Exception("no_end_position_defined")
        return self.end_pos


class Snake(MovingEntity):
    """Represents a snake entity on the game board."""

    def __init__(self, end_pos=None):
        """
        Initialize a Snake object.

        Parameters:
        - end_pos (int, optional): The position where the player will be sent after encountering the snake.
        """
        super(Snake, self).__init__(end_pos)
        self.desc = "Bit by Snake"


class Ladder(MovingEntity):
    """Represents a ladder entity on the game board."""

    def __init__(self, end_pos=None):
        """
        Initialize a Ladder object.

        Parameters:
        - end_pos (int, optional): The position where the player will be sent after climbing the ladder.
        """
        super(Ladder, self).__init__(end_pos)
        self.desc = "Climbed Ladder"


class Board:
    """
    Defines the game board with size and tracks the positions of moving entities.

    Attributes:
    - size: The size of the board.
    - board: A mapping of positions to moving entities.
    """

    def __init__(self, size):
        """
        Initialize a Board object.

        Parameters:
        - size (int): The size of the board.
        """
        self.size = size
        self.board = {}

    def get_size(self):
        """Get the size of the board."""
        return self.size

    def set_moving_entity(self, pos, moving_entity):
        """Set a moving entity at a specified position on the board."""
        self.board[pos] = moving_entity

    def get_next_pos(self, player_pos):
        """
        Get the next position of the player after encountering any moving entity.

        Parameters:
        - player_pos (int): The current position of the player on the board.

        Returns:
        - int: The next position of the player after encountering any moving entity.
        """
        if player_pos > self.size:
            return player_pos
        if player_pos not in self.board:
            return player_pos
        print(f'{self.board[player_pos].desc} at {player_pos}')
        return self.board[player_pos].get_end_pos()

    def at_last_pos(self, pos):
        """
        Check if a position is the last position on the board.

        Parameters:
        - pos (int): The position to check.

        Returns:
        - bool: True if the position is the last position, False otherwise.
        """
        if pos == self.size:
            return True
        return False


class Dice:
    """
    Simulates the rolling of a dice with a given number of sides.

    Attributes:
    - sides: The number of sides in the dice.
    """

    def __init__(self, sides):
        """
        Initialize a Dice object.

        Parameters:
        - sides (int): The number of sides in the dice.
        """
        self.sides = sides

    def roll(self):
        """
        Roll the dice and return the result.

        Returns:
        - int: A random number between 1 to the number of sides on the dice.
        """
        import random
        ans = random.randrange(1, self.sides + 1)
        return ans


class Game:
    """
    Orchestrates the gameplay logic including player movements, turns, and game state.

    Attributes:
    - board: The game board object.
    - dice: The game dice object.
    - players: A list of game player objects.
    - turn: The current turn in the game.
    - winner: The winner of the game.
    - last_rank: The rank achieved by the last player.
    - consecutive_six: The number of consecutive sixes rolled in one turn.
    """

    def __init__(self):
        """
        Initialize a Game object.
        """
        self.board = None
        self.dice = None
        self.players = []
        self.turn = 0
        self.winner = None
        self.last_rank = 0
        self.consecutive_six = 0

    def initialize_game(self, board: Board, dice_sides, players):
        """
        Initialize the game using the provided board, dice, and players.

        Parameters:
        - board (Board): The game board object.
        - dice_sides (int): The number of sides in the dice.
        - players (int): The number of players in the game.
        """
        self.board = board
        self.dice = Dice(dice_sides)
        self.players = [GamePlayer(i) for i in range(players)]

    def can_play(self):
        """
        Check if the game can continue.

        Returns:
        - bool: True if the game can continue, False otherwise.
        """
        if self.last_rank != len(self.players):
            return True
        return False

    def get_next_player(self):
        """
        Get the next player to play.

        Returns:
        - GamePlayer: The next player to play who is still active.
        """
        while True:
            if self.players[self.turn].get_rank() == -1:
                return self.players[self.turn]
            self.turn = (self.turn + 1) % len(self.players)

    def move_player(self, curr_player, next_pos):
        """
        Move the player to the next position on the board.

        Parameters:
        - curr_player (GamePlayer): The current player.
        - next_pos (int): The next position of the player.
        """
        curr_player.set_position(next_pos)
        if self.board.at_last_pos(curr_player.get_pos()):
            curr_player.set_rank(self.last_rank + 1)
            self.last_rank += 1

    def can_move(self, curr_player, to_move_pos):
        """
        Check if the player can move to the specified position.

        Parameters:
        - curr_player (GamePlayer): The current player.
        - to_move_pos (int): The position to move to.

        Returns:
        - bool: True if the player can move to the specified position, False otherwise.
        """
        if to_move_pos <= self.board.get_size() and curr_player.get_rank() == -1:
            return True
        return False

    def change_turn(self, dice_result):
        """
        Change the player turn based on the dice result.

        Parameters:
        - dice_result (int): The result of rolling the dice.
        """
        self.consecutive_six = 0 if dice_result != 6 else self.consecutive_six + 1
        if dice_result != 6 or self.consecutive_six == 3:
            if self.consecutive_six == 3:
                print("Changing turn due to 3 consecutive sixes")
            self.turn = (self.turn + 1) % len(self.players)
        else:
            print(f"One more turn for player {self.turn+1} after rolling 6")

    def play(self):
        """
        Start the game and execute the gameplay logic until a winner is determined.
        """
        while self.can_play():
            curr_player = self.get_next_player()
            player_input = input(
                f"Player {self.turn+1}, Press enter to roll the dice")
            dice_result = self.dice.roll()
            print(f'dice_result: {dice_result}')
            _next_pos = self.board.get_next_pos(
                curr_player.get_pos() + dice_result)
            if self.can_move(curr_player, _next_pos):
                self.move_player(curr_player, _next_pos)
            self.change_turn(dice_result)
            self.print_game_state()
        self.print_game_result()

    def print_game_state(self):
        """Print the state of the game after every turn."""
        print('-------------game state-------------')
        for ix, _p in enumerate(self.players):
            print(f'Player: {ix+1} is at pos {_p.get_pos()}')
        print('-------------game state-------------\n\n')

    def print_game_result(self):
        """Print the final game result with ranks of each player."""
        print('-------------final result-------------')
        for _p in sorted(self.players, key=lambda x: x.get_rank()):
            print(f'Player: {_p._id+1} , Rank: {_p.get_rank()}')


def sample_run():
    """
    Execute a sample run of the game with predefined board configurations and player settings.
    """
    # Create a board of size 10
    board = Board(10)
    # Set snake at position 7 with end position at 2
    board.set_moving_entity(7, Snake(2))
    # Set ladder at position 4 with end position at 6
    board.set_moving_entity(4, Ladder(6))
    # Initialize the game with 2 players and a dice with 6 sides
    game = Game()
    game.initialize_game(board, 6, 2)
    # Start the game
    game.play()


if __name__ == "__main__":
    sample_run()
