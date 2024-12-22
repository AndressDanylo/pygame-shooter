import pygame
import pytmx
import pytmx.util_pygame


class Map:
    def __init__(self, map_file, screen_width, screen_height):
        self.map_file = map_file
        self.tiles = pygame.sprite.Group()
        self.collidable_tiles = pygame.sprite.Group()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pos_x = 0
        self.pos_y = 0

        self.load_map()

    # TODO maybe turn map into a singleton which can reload into diff maps
    def load_map(self):
        tmx_data = pytmx.util_pygame.load_pygame(self.map_file)
        self.tile_size = tmx_data.tilewidth
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight

        self._set_spawn_position(tmx_data)
        self._load_layers(tmx_data)
    
    def _set_spawn_position(self, tmx_data):
         for object in tmx_data.get_layer_by_name("Meta Layer"):
            if object.name == "spawn":
                        self.pos_x = object.x - self.screen_width // 2
                        self.pos_y = object.y - self.screen_height // 2
    
    def _load_layers(self, tmx_data):
        for layer in tmx_data.layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                # Tiles
                for x, y, surface in layer.tiles():
                    gid = tmx_data.get_tile_gid(x, y, tmx_data.layers.index(layer))
                    props = tmx_data.get_tile_properties_by_gid(gid)
                    pos_x = x * tmx_data.tilewidth - self.pos_x
                    pos_y = y * tmx_data.tileheight - self.pos_y
                    tile = Tile((pos_x, pos_y), surface, props, self.tiles)
                    if props.get("collidable"):
                        self.collidable_tiles.add(tile)
            if isinstance(layer, pytmx.TiledObjectGroup):
                # Objects
                for object in layer:
                    pass

    def draw(self, display, pos_x, pos_y):
        display_rect = display.get_rect()
        #display_rect.inflate_ip(-64*4, -64*2)
        for tile in self.tiles:
            tile_rect = tile.rect.move(pos_x, pos_y)
            if display_rect.colliderect(tile_rect):
                display.blit(tile.image, tile_rect)

    def get_collidable_tiles(self):
        return self.collidable_tiles

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, props, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.is_collidable = props.get("collidable", False)
