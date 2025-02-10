import pygame
import pytmx
import pytmx.util_pygame
from pygame import Vector2
from entities import Enemy
import config


class Map:
    def __init__(self, map_file, enemies):
        self.map_file = map_file
        self.tiles = pygame.sprite.Group()
        self.collidable_tiles = pygame.sprite.Group()
        self.spawn_position = Vector2(0, 0)

        self._load_map(enemies)

    # TODO maybe turn map into a singleton which can reload into diff maps
    def _load_map(self, enemies):
        tmx_data = pytmx.util_pygame.load_pygame(self.map_file)
        self.tile_size = tmx_data.tilewidth
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight
        self._load_meta(tmx_data, enemies)
        self._load_layers(tmx_data)
    
    def _load_meta(self, tmx_data, enemies : pygame.sprite.Group):
        for object in tmx_data.get_layer_by_name("Meta Layer"):
            if object.name == "spawn":
                self.spawn_position = Vector2(object.x, object.y)
            elif object.name == "mob":
                enemy = Enemy(Vector2(object.x, object.y))
                enemies.add(enemy)
    
    def _load_layers(self, tmx_data):
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Tiles
                for x, y, surface in layer.tiles():
                    gid = tmx_data.get_tile_gid(x, y, tmx_data.layers.index(layer))
                    props = tmx_data.get_tile_properties_by_gid(gid)
                    pos_x = x * tmx_data.tilewidth
                    pos_y = y * tmx_data.tileheight
                    tile = Tile((pos_x, pos_y), surface, props)
                    self.tiles.add(tile)
                    if props.get("collidable"):
                        self.collidable_tiles.add(tile)
            elif isinstance(layer, pytmx.TiledObjectGroup):
                # make sure to not read meta layer here
                # Objects
                for object in layer:
                    pass

    def get_spawn_position(self):
        return self.spawn_position
    def get_tiles(self):
        return self.tiles
    def get_collidable_tiles(self):
        return self.collidable_tiles

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, props):
        super().__init__()
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.is_collidable = props.get("collidable", False)
