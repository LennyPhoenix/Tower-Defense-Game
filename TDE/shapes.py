from pyglet.graphics import *
from pyglet.gl import *
import main


class Rectangle(object):
    def __init__(self, x, y, width, height, colour=main.Colours.white):
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
