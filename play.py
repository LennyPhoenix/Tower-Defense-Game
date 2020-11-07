from TDE import tde
import tilesets
import res
import main
import maps


BOTTOM_BAR_HEIGHT = 120
TOP_BAR_HEIGHT = 24


FONT_SIZE = 16
FONT_NAME = 'Roboto'
PLAY_BUTTON_TEXT = 'Regenerate'
PLAY_BUTTON_TEXT_FONT = 'Roboto'
PLAY_BUTTON_TEXT_SIZE = 16
PLAY_BUTTON_COLOUR = tde.Colours.white
PLAY_BUTTON_X = 300
PLAY_BUTTON_Y = BOTTOM_BAR_HEIGHT / 2
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
        show(self.screen.window)


def get_screen(window):
    thing = tde.Screen(window)
    bottom_bar = tde.Rectangle(main.WIDTH / 2, BOTTOM_BAR_HEIGHT / 2, main.WIDTH, BOTTOM_BAR_HEIGHT)
    bottom_bar.attach(thing)
    top_bar = tde.Rectangle(main.WIDTH / 2, main.HEIGHT - (TOP_BAR_HEIGHT / 2), main.WIDTH, TOP_BAR_HEIGHT)
    top_bar.attach(thing)
    play_map = maps.Map(thing, tilesets.Fields())
    overlay_button = PlayButton(PLAY_BUTTON_COLOUR,
                             thing,
                             PLAY_BUTTON_X,
                             PLAY_BUTTON_Y,
                             PLAY_BUTTON_WIDTH,
                             PLAY_BUTTON_HEIGHT,
                             PLAY_BUTTON_TEXT,
                             PLAY_BUTTON_TEXT_FONT,
                             PLAY_BUTTON_TEXT_SIZE,
                             PLAY_BUTTON_TEXT_COLOUR)
    return thing


def prepare(window):
    window.set_screen(get_screen(window))


def show(window):
    get_screen(window).show()
