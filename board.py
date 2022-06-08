import random
import arcade


class Board:

    def __init__(self):
        self.b = []  # b = board
        self._all_points = []
        self.exposed = []
        self.flagged = []
        self.mines = []
        self.game_over = False

    def __str__(self):
        """returns a stringed version on the b of the board"""

        string = ""

        for line in self.b:
            for tile in line:
                string += str(tile) + " "
            string += "\n"

        return string

    def gen_board(self, width, height, mine_count):
        """makes a board the size of width*height, with mine_count mines."""
        # 0 = no mine, 1 = mine

        self.b = []

        # fill board with zeroes
        for y in range(height):
            self.b += [[0 for _ in range(width)]]
            self._all_points += [(x, y) for x in range(width)]

        # put mines randomly on the board
        for x, y in random.sample(self._all_points, mine_count):
            self.b[y][x] = 1
            self.mines += [(x, y)]

    def get_value(self, x, y):
        """returns the number of mines around (x,y)"""
        ### THIS FUNCTION ISNT WORKING
        points = [(x + 1, y), (x - 1, y), (x + 1, y + 1),
                  (x + 1, y - 1), (x - 1, y + 1),
                  (x - 1, y - 1), (x, y + 1), (x, y - 1)]
        value = 0
        
        for p in points:
            left = p[0] == -1
            right = p[0] == len(self.b[0])
            up = p[1] == -1
            down = p[1] == len(self.b)
            if not(left or right or up or down):
                value += self.b[p[1]][p[0]]

        return value


    def display(self, running=True):
        """displays the board using arcade"""

        if not running:
            self.exposed += self.mines
        for point in self._all_points:
            if point in self.flagged:
                name = "flag"
            elif point in self.exposed:
                if self.b[point[1]][point[0]] == 1:
                    name = "mine"
                elif self.b[point[1]][point[0]] == 0:
                    name = str(self.get_value(point[0], point[1]))
            else:
                name = "unexplored"
            tile = arcade.load_texture("images/" + name + ".png")
            arcade.draw_texture_rectangle(50 + 100 * point[0],
                                          50 + 100 * point[1],
                                          100, 100, tile)


    def expose(self, x, y):
        """left click at (x,y)"""

        if (x, y) not in self.exposed and (x, y) not in self.flagged:

            self.exposed += [(x, y)]
            
            if self.get_value(x, y) == 0:
                self.show_zeroes()
            if len(self.exposed) + len(self.mines) == len(self._all_points):
                    self.game_over = True
            if self.b[y][x] == 1:
                self.death()

    def death(self):
        self.game_over = True

    def all_mines_flagged(self):

        if len(self.flagged) == len(self.mines):
            for flag in self.flagged:
                if flag not in self.mines:
                    return False
        return True

    def check_victory(self):

        if self.all_mines_flagged():
            self.game_over = True

    def show_zeroes(self):
        """when the player finds a 0 tile, this function will auto expose
all zeroes connected."""
        for point1 in self.exposed:
            x = point1[0]
            y = point1[1]
            if self.get_value(x, y) == 0:
                points = [(x + 1, y), (x - 1, y), (x + 1, y + 1),
                          (x + 1, y - 1), (x - 1, y + 1),
                          (x - 1, y - 1), (x, y + 1), (x, y - 1)]
                for p in points:
                    left = p[0] == -1
                    right = p[0] == len(self.b)
                    up = p[1] == -1
                    down = p[1] == len(self.b[0])
                    if not(left or right or up or down):
                        if p not in self.exposed:
                            self.exposed += [p]

                
    def flag(self, x, y):
        """right click at (x,y)"""

        if (x, y) not in self.exposed:
            if (x, y) not in self.flagged:
                self.flagged += [(x, y)]
            else:
                self.flagged.remove((x, y))
