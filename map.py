import pygame
import pytmx
import pytmx.util_pygame

class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.tiles = pygame.sprite.Group()
        self.height, self.width = 0, 0

        tmx_data = pytmx.util_pygame.load_pygame(self.map_file)
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight
        for layer in tmx_data.visible_layers:
            for x, y, surface in layer.tiles():
                gid = tmx_data.get_tile_gid(x, y, tmx_data.layers.index(layer))
                props = tmx_data.get_tile_properties_by_gid(gid)
                pos_x = x * tmx_data.tilewidth - self.width // 2
                pos_y = y * tmx_data.tileheight - self.height // 2
                Tile((pos_x, pos_y), surface, props, self.tiles)
    
    def draw(self, surface, pos_x, pos_y):
        # TODO to make this performant get tiles that are only near the camera. maybe get screen rect that gets put to x,y and check what tiles collide???
        for sprite in self.tiles:
            rect = sprite.rect.move(pos_x, pos_y)
            surface.blit(sprite.image, rect)
        #self.tiles.draw(surface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, props, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.isCcollidable = props.get("collidable")
