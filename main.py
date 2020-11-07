from TDE import tde
import mainmenu
import tilesets
import play


# Globals
WIDTH = 1280
HEIGHT = 720
NAME = 'Insert name here'


if __name__ == '__main__':
    game = tde.Window(WIDTH, HEIGHT, NAME)
    mx, my = WIDTH / 2, HEIGHT / 2  # Middle X and Y (identify the mid point of the window)
    mainmenu.prepare(game)
    tde.start()
