import pyglet
from pyglet.gl import *
from shapes import *
import pygletresources as pygr


# GLOBALS #
WIDTH = 1280
HEIGHT = 720
WINDOW_NAME = 'Game'


def cset(thing):
    e = []
    for i in range(4):
        e += thing
    return 'c3B', e


class Colours:
    white = cset([255, 255, 255])
    black = cset([0, 0, 0])
    red = cset([255, 0, 0])
    blue = cset([0, 0, 255])
    yellow = cset([255, 0, 255])
    green = cset([0, 255, 0])

    def custom(r, g, b):
        return cset([r, g, b])


class Sprite(object):
    def __init__(self, screen, image, x, y):
        self._sprite = pyglet.sprite.Sprite(image, x, y, batch=screen.sprite_batch)
        # Center
        self.x = x
        self.y = y

    def update_image(self, image):
        self._sprite.image = image

    def on_draw(self):
        self._sprite.draw()


class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.active_window = None

    def set_screen(self, screen):
        self.active_window = screen

    def on_draw(self):
        if self.active_window:
            self.active_window.show()
        #print('Window got drawn!')

    def on_mouse_press(self, x, y, button, mod):
        if button == 1:
            if self.active_window:
                self.active_window.on_mouse_press(x, y, button)

    def on_mouse_release(self, x, y, button, mod):
        if button == 1:
            if self.active_window:
                self.active_window.on_mouse_release(x, y, button)

    def on_mouse_drag(self, x, y, dx, dy, buttons, mod):
        if buttons & 1:
            if self.active_window:
                self.active_window.on_mouse_movement(x, y)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.active_window:
            self.active_window.on_mouse_movement(x, y)


class Screen(object):
    def __init__(self, window, background_image=None):
        self.buttons = []
        self.window = window
        self.sprite_batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.foreground = pyglet.graphics.OrderedGroup(1)

    def show(self):
        self.window.active_window = self
        self.window.clear()
        self.sprite_batch.draw()
        for button in self.buttons:
            button.on_draw()

    def on_mouse_movement(self, x, y):
        for button in self.buttons:
            if button.check(x, y):
                if not button.mouse_on_me:
                    button.mouseover()
            else:
                if button.mouse_on_me:
                    button.mouseoff()

    def on_mouse_press(self, x, y, button):
        if button == 1:
            for button in self.buttons:
                if button.check(x, y):
                    button.on_mouse_down()

    def on_mouse_release(self, x, y, button):
        if button == 1:
            for button in self.buttons:
                if button.check(x, y):
                    button.on_mouse_up()
                    button.mouseover()
                elif button.mouse_on_me:
                    button.mouseoff()


class Button(object):
    def __init__(self, screen, x, y, width, height, enabled=True):
        if self not in screen.buttons:
            screen.buttons.append(self)
        self.screen = screen
        self.window = screen.window
        self.enabled = enabled
        self.mouse_on_me = False
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.x1 = x - (width / 2)
        self.y1 = y + (height / 2)
        self.x2 = x + (width / 2)
        self.y2 = y - (height / 2)

    def check(self, x, y):
        if self.x1 < x < self.x2 and self.y2 < y < self.y1:
            return True
        return False

    def on_draw(self):
        print('Button got drawn!')

    def on_mouse_down(self):
        print('mouse down')

    def on_mouse_up(self):
        print('mouse up')

    def mouseover(self):
        self.mouse_on_me = True
        self.on_mouse_over()

    def mouseoff(self):
        self.mouse_on_me = False
        self.on_mouse_off()

    def on_mouse_over(self):
        print('mouse over')

    def on_mouse_off(self):
        print('mouse off')


class RectangleButton(Button):
    def __init__(self, colour, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rect = Rectangle(self.x, self.y, self.w, self.h, colour)

    def on_draw(self):
        self.rect.draw()

    def set_colour(self, colour):
        self.rect.vert.colors = colour[1]

    def on_mouse_over(self):
        print('overwrite mouseover')
        self.set_colour(Colours.yellow)

    def on_mouse_off(self):
        print('overwrite mouse off')
        self.set_colour(Colours.white)

    def on_mouse_down(self):
        print('overwrite click')
        self.set_colour(Colours.blue)

    def on_mouse_up(self):
        print('overwrite release')
        self.set_colour(Colours.white)


class SpriteButton(Button):
    def __init__(self, screen, image, x, y, enabled=True):
        super().__init__(screen, x, y, image.width, image.height, enabled)
        self.sprite = Sprite(self.screen, image, x, y)

    def update_position(self, x=None, y=None):
        if x:
            self.x = x
            self.sprite.x = x
        if y:
            self.y = y
            self.sprite.y = y

    def on_draw(self):
        return

    def on_mouse_over(self):
        print('overwrite mouseover')

    def on_mouse_off(self):
        print('overwrite mouse off')

    def on_mouse_down(self):
        print('overwrite click')

    def on_mouse_up(self):
        print('overwrite release')


if __name__ == '__main__':
    gwindow = Window(WIDTH, HEIGHT, WINDOW_NAME)
    tx = WIDTH / 2
    ty = HEIGHT / 2
    W = 200
    H = 50
    test_image = pygr.image('redtest.png')
    test_mouseover = pygr.image('mouseover.png')
    test_click = pygr.image('click.png')
    test_screen = Screen(gwindow)
    test_button = SpriteButton(test_screen, test_image, tx, ty)
    gwindow.set_screen(test_screen)
    pyglet.app.run()
