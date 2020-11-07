import pyglet
from TDE import tde
import os


def path(name, category=None):
    return 'Resources/'+category+'/'+name if category else 'Resources/' + name


def get_image(name, category=None):
    return tde.image(path(name, category))


def get_cimage(name, category=None):
    return tde.corner_image(path(name, category))


class MainMenu:
    c = 'mainmenu'
    # print(os.getcwd())
    bg = get_cimage('bg.png', c)
