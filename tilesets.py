from TDE import tde
import pyglet
import random
import main


MAP_SIZE = 20, 18  # each side of the field is 40 x 35 tiles

map_pixels = (int(MAP_SIZE[0] * 16), int(MAP_SIZE[1] * 16))
total_width = int(map_pixels[0] * 2)
total_height = int(map_pixels[1])


def path(name, category=None):
    return 'Resources/'+category+'/'+name if category else 'Resources/' + name


def get_image(name, category=None):
    return tde.image(path(name, category))


def from_tileset(tileset, relative_x, relative_y):
    return tileset.get_region(int(relative_x * 16), int(relative_y * 16), 16, 16)


def get_cimage(name, category=None):
    return tde.corner_image(path(name, category))


class Fields(object):
    def __init__(self):
        self.c = 'fields'
        c = self.c
        self.path_1 = get_cimage('path1.png', c)
        self.path_2 = get_cimage('path2.png', c)
        self.grass_1 = get_cimage('grass1.png', c)
        self.grass_2 = get_cimage('grass2.png', c)

        self.br1 = get_cimage('path1_BR.png', c)
        self.br2 = get_cimage('path2_BR.png', c)
        self.lb1 = get_cimage('path1_LB.png', c)
        self.lb2 = get_cimage('path2_LB.png', c)
        self.tb1 = get_cimage('path1_TB.png', c)
        self.tb2 = get_cimage('path2_TB.png', c)

    def get_image_from_code(self, code):
        codes = {
            'BR': random.choice([self.br1, self.br2]),
            'LB': random.choice([self.lb1, self.lb2]),
            'TB': random.choice([self.tb1, self.tb2])
        }
        if code in codes:
            return codes[code]
