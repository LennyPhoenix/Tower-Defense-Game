import pyglet
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
from pyglet.graphics import *


def image(path):
    thing = pyglet.resource.image(path)
    thing.anchor_x = thing.width // 2
    thing.anchor_y = thing.height // 2
    return thing


def corner_image(path):
    thing = pyglet.resource.image(path)
    return thing


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


class Rectangle(object):
    def __init__(self, x, y, width, height, colour=Colours.white):
        self.top_left = (x - (width / 2), y + (height / 2), 0.0)
        self.bottom_right = (x + (width / 2), y - (height / 2), 0.0)
        self.top_right = (self.bottom_right[0], self.top_left[1], 0.0)
        self.bottom_left = (self.top_left[0], self.bottom_right[1], 0.0)
        vertices = []
        vertices += self.bottom_left + self.bottom_right + self.top_right + self.top_left
        self.vert = vertex_list_indexed(4, [0, 1, 2,  2, 3, 0],
                                        ('v3f', vertices),
                                        colour)

    def set_colour(self, colour):
        self.vert.colors = colour

    def draw(self):
        self.vert.draw(GL_TRIANGLES)

    def attach(self, screen):
        screen.things.append(self)


class Sprite(object):
    def __init__(self, screen, image, x, y, background=True, front=False):
        x = int(x)
        y = int(y)
        if front:
            self._sprite = pyglet.sprite.Sprite(image, x, y, batch=screen.sprite_batch, group=screen.front)
        elif background:
            self._sprite = pyglet.sprite.Sprite(image, x, y, batch=screen.sprite_batch, group=screen.background)
        else:
            self._sprite = pyglet.sprite.Sprite(image, x, y, batch=screen.sprite_batch, group=screen.foreground)
        #print(self._sprite.batch)
        # Center
        self.x = x
        self.y = y
        self._sprite.opacity = 255

    def scale(self, amount: float):
        self._sprite.update(scale=amount)

    def update_image(self, pic):
        if not pic:
            return
        self._sprite.image = pic

    def draw(self):
        self.on_draw()

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
        self.front = pyglet.graphics.OrderedGroup(2)
        self.bg = background_image
        self.things = []
        self.thing = []
        if self.bg:
            self.bg_sprite = Sprite(self, self.bg, 0, 0)

    def show(self):
        self.window.active_window = self
        self.window.clear()
        #if self.thing:
        #    print(self.sprite_batch == self.thing.batch)
        self.sprite_batch.draw()
        for thing in self.things:
            thing.draw()
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
    def __init__(self, screen, x, y, width, height, enabled=True, text=None, text_font='Roboto', text_size=16,
                 text_colour=(255, 255, 255, 255)):
        if self not in screen.buttons:
            screen.buttons.append(self)
        if text:
            self.text = pyglet.text.Label(text,
                                          font_name=text_font,
                                          font_size=text_size,
                                          x=x,
                                          y=y,
                                          anchor_x='center',
                                          anchor_y='center',
                                          color=text_colour)
        else:
            self.text = None
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
        self.draw()
        if self.text:
            self.text.draw()

    def draw(self):
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
    def __init__(self, colour, outline_size=0, outline_colour=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.out_size = outline_size
        self.out_colour = outline_colour
        if self.out_size > 0:
            self.outline = Rectangle(
                self.x,
                self.y,
                self.w + (2*self.out_size),
                self.h + (2*self.out_size),
                self.out_colour
            )
        else:
            self.outline = None
        self.rect = Rectangle(self.x, self.y, self.w, self.h, colour)

    def draw(self):
        if self.outline:
            self.outline.draw()
        self.rect.draw()

    def set_colour(self, colour):
        self.rect.vert.colors = colour[1]

    def set_outline_colour(self, colour):
        self.outline.vect.colors = colour[1]


class SpriteButton(Button):
    def __init__(self, screen, image, x, y, enabled=True):
        super().__init__(screen, x, y, image.width, image.height, enabled)
        self.image = image
        self.sprite = Sprite(self.screen, image, x, y)

    def draw(self):
        return

    def on_mouse_over(self):
        print('overwrite mouseover')

    def on_mouse_off(self):
        print('overwrite mouse off')

    def on_mouse_down(self):
        print('overwrite click')

    def on_mouse_up(self):
        print('overwrite release')


class InteractiveButton(SpriteButton):
    def __init__(self, mouse_over_image, click_image, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moimage = mouse_over_image
        self.cimage = click_image

    def on_mouse_over(self):
        self.sprite.update_image(self.moimage)

    def on_mouse_down(self):
        self.sprite.update_image(self.cimage)

    def on_mouse_off(self):
        self.sprite.update_image(self.image)
        self.on_click()

    def on_mouse_up(self):
        self.sprite.update_image(self.moimage)

    def on_click(self):
        print('ive been clicked!')


if __name__ == '__main__':
    gwindow = Window(WIDTH, HEIGHT, WINDOW_NAME)
    tx = WIDTH / 2
    ty = HEIGHT / 2
    W = 200
    H = 50
    test_image = image('redtest.png')
    test_mouseover = image('mouseover.png')
    test_click = image('click.png')
    test_screen = Screen(gwindow)
    test_button = InteractiveButton(test_mouseover, test_click, test_screen, test_image, tx, ty)
    gwindow.set_screen(test_screen)
    pyglet.app.run()
