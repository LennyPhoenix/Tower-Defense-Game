import pyglet


def image(path):
    thing = pyglet.image.load(path)
    thing.anchor_x = thing.width // 2
    thing.anchor_y = thing.height // 2
    return thing
