from board import Board
import random
import arcade

rows = 9
cols = rows
window_height = rows * 100
window_width = int((window_height / rows) * cols)
mine_count = 15


class MineSweeper(arcade.Window):

    def __init__(self):
        super().__init__(window_width, window_height, "MINE SWEEPER")
        # self.b;

    def setup(self):
        # arcade.open_window(800, 800, "")
        # arcade.set_background_color((0, 0, 0))
        # self.b.init_display()
        # print("setup call")
        # self.b.display()
        self.b = Board()
        self.b.gen_board(cols, rows, mine_count)
        self.running = True

    def on_draw(self):
        # pass
        # print("drawing")
        self.b.display(self.running)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """logic?"""

        if self.running:
            if button == arcade.MOUSE_BUTTON_LEFT:
                self.b.expose(x // 100, y // 100)
            if button == arcade.MOUSE_BUTTON_RIGHT:
                self.b.flag(x // 100, y // 100)

            if self.b.game_over:
                self.running = False
        else:
            self.setup()

##        self.b.display(self.running)


def main():
    """ Main method """
    window = MineSweeper()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
