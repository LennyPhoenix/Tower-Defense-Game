from TDE import tde
import res
import main


FONT_SIZE = 16
FONT_NAME = 'Roboto'
PLAY_BUTTON_TEXT = 'Play'
PLAY_BUTTON_TEXT_FONT = 'Roboto'
PLAY_BUTTON_TEXT_SIZE = 16
PLAY_BUTTON_COLOUR = tde.Colours.white
PLAY_BUTTON_X = main.WIDTH / 2
PLAY_BUTTON_Y = main.HEIGHT / 2
PLAY_BUTTON_WIDTH = 200
PLAY_BUTTON_HEIGHT = 50
PLAY_BUTTON_OUTLINE_SIZE = 5
PLAY_BUTTON_OUTLINE_COLOUR = tde.Colours.black
PLAY_BUTTON_TEXT_COLOUR = (0, 0, 0, 255)


class PlayButton(tde.RectangleButton):
    def __init__(self, colour, screen, x, y, width, height, text=None, text_font='Roboto', text_size=16,
                 text_colour=(255, 255, 255, 255)):
        super().__init__(colour, PLAY_BUTTON_OUTLINE_SIZE, PLAY_BUTTON_OUTLINE_COLOUR, screen, x, y, width, height,
                         text_font=text_font, text_size=text_size, text=text, text_colour=text_colour)

    def on_mouse_over(self):
        self.set_colour(tde.Colours.custom(178, 178, 178))

    def on_mouse_off(self):
        self.set_colour(tde.Colours.white)

    def on_mouse_down(self):
        self.set_colour(tde.Colours.custom(119, 119, 119))

    def on_mouse_up(self):
        main.play.show(self.screen.window)


def get_screen(window):
    thing = tde.Screen(window, res.MainMenu.bg)
    play_button = PlayButton(PLAY_BUTTON_COLOUR,
                             thing,
                             PLAY_BUTTON_X,
                             PLAY_BUTTON_Y,
                             PLAY_BUTTON_WIDTH,
                             PLAY_BUTTON_HEIGHT,
                             PLAY_BUTTON_TEXT,
                             PLAY_BUTTON_TEXT_FONT,
                             PLAY_BUTTON_TEXT_SIZE,
                             PLAY_BUTTON_TEXT_COLOUR)
    #tde.SpriteButton(thing, res.Tileset.GrassFields.grass_1, main.WIDTH / 2, main.HEIGHT / 2)
    return thing


def prepare(window):
    window.set_screen(get_screen(window))


def show(window):
    get_screen(window).show()
