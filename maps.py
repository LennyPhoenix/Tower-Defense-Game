from TDE import tde
import pyglet
import main
import random


UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3


def format_coords(x, y):
    return x * 32, y * 32 + main.play.BOTTOM_BAR_HEIGHT


class TileType(object):
    pass


class PathTile(TileType):
    pass


class TerrainTile(TileType):
    pass


class Map(object):
    def __init__(self, screen, tileset):
        # When generating a map, first thing to do is generate the plain baseline of grass
        self.tiles = []
        self.screen = screen
        self.tileset = tileset
        self.path_tiles = [self.tileset.path_1, self.tileset.path_2]
        self.grass_tiles = [self.tileset.grass_1, self.tileset.grass_2]
        for x in range(40):
            for y in range(18):
                self.tiles.append(create_tile(self.get_grass_image(), TerrainTile, x, y, screen, self))
        self._generate_path()

    def get_tile(self, rx, ry):
        for tile in self.tiles:
            if tile.relative_x == rx and tile.relative_y == ry:
                yield tile

    def remove_tile(self, relative_x, relative_y):
        for tile in self.tiles:
            if tile.relative_x == relative_x and tile.relative_y == relative_y:
                tile.remove()
                self.tiles.remove(tile)

    def new_tile(self, rx, ry, ttype, image, overlay=False):
        if not overlay:
            for tile in self.get_tile(rx, ry):
                tile.remove()
                self.tiles.remove(tile)
        t = create_tile(image, ttype, rx, ry, self.screen, self, overlay)
        self.tiles.append(t)
        return t

    def replace_path(self, tile):
        return self.create_path(tile.rx, tile.ry)

    def get_path_image(self):
        return random.choice(self.path_tiles)

    def get_grass_image(self):
        return random.choice(self.grass_tiles)

    def create_path(self, rx, ry):
        return self.new_tile(rx, ry, PathTile, self.get_path_image())

    def is_terrain(self, rx, ry):
        for tile in self.get_tile(rx, ry):
            if tile.tile_type != TerrainTile:
                return False
        return True

    def remove_if_terrain(self, rx, ry):
        for tile in self.get_tile(rx, ry):
            if tile.tile_type == TerrainTile:
                tile.remove()
                self.tiles.remove(tile)
            else:
                return False
        return True

    def _generate_path(self):
        # First we start in the middle somewhere
        ry = random.randint(1, 16)
        last_tile = None
        for i in range(random.randint(6, 7)):
            rx = 19 - i
            for tile in self.get_tile(rx, ry):
                if tile.terrain():
                    tile.remove()
                    self.tiles.remove(tile)
            last_tile = self.create_path(rx, ry)

        target_x = random.randint(3, 5)
        target_y = random.randint(3, 16)
        target2_x = random.randint(7, 11)
        options = list(range(3, 15))
        if ry in options:
            options.remove(ry)
        if ry + 1 in options:
            options.remove(ry + 1)
        if ry - 1 in options:
            options.remove(ry - 1)
        if ry - 2 in options:
            options.remove(ry - 2)
        if ry + 2 in options:
            options.remove(ry + 2)
        if target_y in options:
            options.remove(target_y)
        if target_y + 1 in options:
            options.remove(target_y + 1)
        if target_y - 1 in options:
            options.remove(target_y - 1)
        target2_y = random.choice(options)
        target_tile = self.create_path(target_x, target_y)
        target2_tile = self.create_path(target2_x, target2_y)
        end_x = 19
        choices = list(range(1, 16))
        if ry in choices:
            choices.remove(ry)
        if ry + 1 in choices:
            choices.remove(ry + 1)
        if ry - 1 in choices:
            choices.remove(ry - 1)
        end_y = random.choice(choices)
        end_tile = self.create_path(end_x, end_y)
        baseline = last_tile
        print(target_x)
        print(target_y)
        print(target2_x)
        print(target2_y)
        if last_tile.ry > end_y:
            print('Map variant A')
            if 17 - last_tile.ry > 5:
                for i in range(random.randint(1, 4)):
                    last_tile = self.replace_path(last_tile.above())
                if last_tile.ry - 1 in [target2_y, target_y]:
                    last_tile = self.replace_path(last_tile.above())
            if last_tile.ry > target_y and last_tile.ry > target2_y:
                print('Map class 1')
                last_tile = self.replace_path(last_tile.left())
                last_tile = self.replace_path(last_tile.left())
                last_tile = self.pathx(last_tile, target_x)
                last_tile = self.pathy(last_tile, target_y)
                last_tile = self.replace_path(last_tile.below())
                last_tile = self.pathx(last_tile, target2_x)
                last_tile = self.pathy(last_tile, target2_y)
                last_tile = self.replace_path(last_tile.right())
                last_tile = self.replace_path(last_tile.right())
                last_tile = self.pathy(last_tile, end_y)
                last_tile = self.pathx(last_tile, end_x)
            elif last_tile.ry > target2_y:
                print('Map class 2')
                if last_tile.ry < target_y:
                    last_tile = self.pathy(last_tile, target_y)
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x)
                elif target_y > target2_y:
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x)

            else:
                if last_tile.rx - 3 > target2_x:
                    print('Map class 3')
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, target_y)
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.replace_path(last_tile.below())
                    last_tile = self.replace_path(last_tile.below())
                    if last_tile.ry + 1 == baseline.ry:
                        last_tile = self.replace_path(last_tile.below())
                    if last_tile.ry > baseline.ry or last_tile.ry == baseline.ry:
                        last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x - 1)
                    last_tile = self.pathy(last_tile, end_y)
                else:
                    print('Map class 4')
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.pathy(last_tile, target_y)
                    if not last_tile.below().terrain():
                        last_tile = self.replace_path(last_tile.left())
                        last_tile = self.replace_path(last_tile.left())
                        last_tile = self.pathy(last_tile, end_y)
                        last_tile = self.pathx(last_tile, end_x)
                    else:
                        if last_tile.ry > 3:
                            last_tile = self.replace_path(last_tile.below())
                            last_tile = self.replace_path(last_tile.below())
                        last_tile = self.replace_path(last_tile.right())
                        last_tile = self.replace_path(last_tile.right())
                        last_tile = self.pathy(last_tile, end_y)
                        last_tile = self.pathx(last_tile, end_x)
        else:
            print('Map variant B')
            if target_y >= end_y:
                if target2_y < target_y:
                    print('Map class 1')
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.pathy(last_tile, target_y)
                    last_tile = self.pathx(last_tile, end_x - 1)
                    last_tile = self.pathy(last_tile, end_y)
                else:
                    print('Map class 1a')
                    last_tile = self.pathx(last_tile, target_x)
                    last_tile = self.pathy(last_tile, target_y)
                    last_tile = self.pathy(last_tile, target2_y)
                    last_tile = self.pathx(last_tile, target2_x)
                    last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x)
            elif target_y < target2_y:
                print('Map class 2')
                last_tile = self.pathy(last_tile, target_y)
                last_tile = self.pathx(last_tile, target_x)
                last_tile = self.pathy(last_tile, target2_y)
                last_tile = self.pathx(last_tile, target2_x)
                if last_tile.ry < baseline.ry:
                    last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x)
                else:
                    last_tile = self.pathx(last_tile, end_x - random.randint(1, 3))
                    last_tile = self.pathy(last_tile, end_y)
                    last_tile = self.pathx(last_tile, end_x)
            elif target2_y < target_y:
                print('Map class 3')
                last_tile = self.pathy(last_tile, target2_y)
                last_tile = self.pathx(last_tile, target2_x)
                last_tile = self.pathx(last_tile, target_x)
                last_tile = self.pathy(last_tile, target_y)
                last_tile = self.pathy(last_tile, end_y)
                last_tile = self.pathx(last_tile, end_x)

        # Now it's time to mirror the path
        for tile in self.tiles.copy():
            if tile.tile_type != PathTile:
                continue
            new_rx = 39 - tile.rx
            self.create_path(new_rx, tile.ry)

        for tile in self.tiles:
            if tile.path():
                tile.update()

    def pathx(self, tile, rx):
        if tile.rx == rx:
            return tile
        if tile.rx > rx:
            while tile.rx > rx and tile.left().terrain():
                tile = self.replace_path(tile.left())
            if not tile.left().terrain():
                tile = tile.left()
        else:
            while tile.rx < rx and tile.right().terrain():
                tile = self.replace_path(tile.right())
            if not tile.right().terrain():
                tile = tile.right()
        return tile

    def pathy(self, tile, ry):
        if tile.ry == ry:
            return tile
        if tile.ry > ry:
            while tile.ry > ry and tile.below().terrain():
                tile = self.replace_path(tile.below())
            if not tile.below().terrain():
                tile = tile.below()
        else:
            while tile.ry < ry and tile.above().terrain():
                tile = self.replace_path(tile.above())
            if not tile.above().terrain():
                tile = tile.above()
        return tile

    def _generate_bush(self, image):
        options = []
        for tile in self.tiles:
            if tile.terrain():
                options.append(tile)
        tile = random.choice(options)
        self.tiles.append(create_tile(image, TerrainTile, tile.rx, tile.ry, self.screen, self, True))


def create_tile(image, tile_type, relative_x, relative_y, screen, map: Map, overlay=False):
    x = relative_x * 32
    y = (relative_y * 32) + main.play.BOTTOM_BAR_HEIGHT
    spr = tde.Sprite(screen, image, int(x), int(y), not overlay)
    spr.scale(2)
    screen.thing.append(spr)
    tile = Tile(spr, tile_type, map)
    return tile


class Tile(object):
    def __init__(self, sprite, tile_type, map: Map):
        self.tile_type = tile_type
        self._sprite = sprite
        self.map = map
        self.x, self.y = sprite._sprite.position
        self.relative_x, self.relative_y = self.x / 32, (self.y - main.play.BOTTOM_BAR_HEIGHT) / 32
        self.rx, self.ry = self.relative_x, self.relative_y
        self.directions = None
        self.UP = 0
        self.LEFT = 1
        self.DOWN = 2
        self.RIGHT = 3
        self._cached_invalid_tiles = []

    def remove(self):
        self._sprite._sprite.delete()

    def direction(self, id):
        t = {
            UP: self.above,
            DOWN: self.below,
            LEFT: self.left,
            RIGHT: self.right
        }
        if id in t:
            return t[id]()

    def check_directions(self):
        directions = [self.LEFT, self.UP, self.RIGHT, self.DOWN]
        if self.at_left():
            directions.remove(self.LEFT)
        if self.at_bottom():
            directions.remove(self.DOWN)
        if self.at_top():
            directions.remove(self.UP)
        if self.at_right():
            directions.remove(self.RIGHT)
        self.directions = directions

    def invert_direction(self, direction):
        if direction == self.RIGHT:
            return self.LEFT
        if direction == self.DOWN:
            return self.UP
        if direction == self.LEFT:
            return self.RIGHT
        if direction == self.UP:
            return self.DOWN

    def adjacent_to(self, tile_type, excluding=None):
        if excluding is None:
            excluding = []
        self.check_directions()
        dd = self.directions.copy()
        for thing in excluding:
            if thing in dd:
                dd.remove(thing)
        if len(dd) == 0:
            return False
        for direction in dd:
            if self.direction(direction).tile_type == tile_type:
                return True
        return False

    def above(self):
        #print(self.rx, self.ry)
        #print(self.map)
        #print(list(self.map.get_tile(self.rx, self.ry + 1)))
        e = list(self.map.get_tile(self.rx, self.ry + 1))
        if len(e) > 0:
            return e[0]

    def below(self):
        #print(self.rx, self.ry)
        #print(self.map)
        #print(list(self.map.get_tile(self.rx, self.ry - 1)))
        e = list(self.map.get_tile(self.rx, self.ry - 1))
        if len(e) > 0:
            return e[0]

    def left(self):
        #print(self.rx, self.ry)
        #print(self.map)
        #print(list(self.map.get_tile(self.rx - 1, self.ry)))
        e = list(self.map.get_tile(self.rx - 1, self.ry))
        if len(e) > 0:
            return e[0]

    def right(self):
        #print(self.rx, self.ry)
        #print(self.map)
        #print(list(self.map.get_tile(self.rx + 1, self.ry)))
        e = list(self.map.get_tile(self.rx + 1, self.ry))
        if len(e) > 0:
            return e[0]


    def update(self):
        name = ''
        if self.above().path():
            name += 'T'
        if self.left().path():
            name += 'L'
        if self.below().path():
            name += 'B'
        if self.right().path():
            name += 'R'
        self._sprite.update_image(self.map.tileset.get_image_from_code(name))

    def at_top(self):
        return self.ry == 17

    def at_bottom(self):
        return self.ry == 0

    def at_left(self):
        return self.rx == 0

    def at_right(self):
        return self.rx == 39

    def on_right(self):
        return self.rx > 19

    def on_left(self):
        return not self.on_right()

    def path(self):
        return self.tile_type == PathTile

    def terrain(self):
        return self.tile_type == TerrainTile
