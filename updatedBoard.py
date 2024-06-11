import turtle

# Constants
BOARD_SIZE = 10
SQUARE_SIZE = 50
START_POS = (-250, -250)
SNAKES = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
LADDERS = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}


class BoardDrawer:
    """
    Class to draw the Snake and Ladder game board using Turtle graphics.
    """

    def __init__(self, size):
        """
        Initialize the BoardDrawer object.

        Parameters:
        - size (int): The size of the board.
        """
        self.size = size
        self.screen = turtle.Screen()
        self.screen.title("Snake and Ladder Board")
        self.screen.setup(width=600, height=600)
        self.pen = turtle.Turtle()
        self.pen.speed(0)
        self.pen.penup()
        self.pen.goto(*START_POS)
        self.pen.pendown()

    def draw_square(self, x, y, size, number):
        """
        Draw a square on the board.

        Parameters:
        - x (int): The x-coordinate of the bottom-left corner of the square.
        - y (int): The y-coordinate of the bottom-left corner of the square.
        - size (int): The size of the square.
        - number (int): Number to be displayed inside the square.
        """
        self.pen.penup()
        self.pen.goto(x, y)
        self.pen.pendown()
        self.pen.begin_fill()
        for _ in range(4):
            self.pen.forward(size)
            self.pen.left(90)
        self.pen.end_fill()
        self.pen.penup()
        self.pen.goto(x + size // 2, y + size // 2 - 10)
        self.pen.write(number, align="center", font=("Arial", 12, "normal"))

    def draw_board(self):
        """
        Draw the Snake and Ladder game board.
        """
        counter = 1
        for i in range(self.size):
            for j in range(self.size):
                x = START_POS[0] + (i * SQUARE_SIZE)
                y = START_POS[1] + (j * SQUARE_SIZE)
                if (i + j) % 2 == 0:
                    self.pen.color("lightblue")
                else:
                    self.pen.color("lightgreen")
                self.draw_square(x, y, SQUARE_SIZE, counter)
                counter += 1
        self.draw_snakes_and_ladders()

    def draw_snakes_and_ladders(self):
        """
        Draw snakes and ladders on the board.
        """
        for start, end in SNAKES.items():
            self.draw_arrow(start, end, "red")
        for start, end in LADDERS.items():
            self.draw_arrow(start, end, "green")

    def draw_arrow(self, start, end, color):
        """
        Draw an arrow from start to end position.

        Parameters:
        - start (int): Start position of the arrow.
        - end (int): End position of the arrow.
        - color (str): Color of the arrow.
        """
        start_x = START_POS[0] + ((start - 1) % self.size) * SQUARE_SIZE + SQUARE_SIZE // 2
        start_y = START_POS[1] + ((start - 1) // self.size) * SQUARE_SIZE + SQUARE_SIZE // 2
        end_x = START_POS[0] + ((end - 1) % self.size) * SQUARE_SIZE + SQUARE_SIZE // 2
        end_y = START_POS[1] + ((end - 1) // self.size) * SQUARE_SIZE + SQUARE_SIZE // 2

        self.pen.penup()
        self.pen.goto(start_x, start_y)
        self.pen.pendown()
        self.pen.color(color)

        # Draw a wavy line
        self.pen.width(3)
        distance = ((end_x - start_x) ** 2 + (end_y - start_y) ** 2) ** 0.5
        waves = int(distance / 10)
        for _ in range(waves):
            self.pen.forward(10)
            self.pen.left(30)
            self.pen.forward(10)
            self.pen.right(60)
            self.pen.forward(10)
            self.pen.left(30)
            self.pen.forward(10)

        # Draw the arrow head
        self.pen.setheading(self.pen.towards(end_x, end_y))
        self.pen.right(90)
        self.pen.forward(20)
        self.pen.right(150)
        self.pen.forward(30)
        self.pen.left(120)
        self.pen.forward(30)
        self.pen.left(150)
        self.pen.forward(20)

        # Write the label
        self.pen.penup()
        self.pen.goto((start_x + end_x) / 2, (start_y + end_y) / 2 + 5)
        self.pen.write(str(start) + "->" + str(end), align="center", font=("Arial", 8, "normal"))


if __name__ == "__main__":
    board_drawer = BoardDrawer(BOARD_SIZE)
    board_drawer.draw_board()
    turtle.done()
