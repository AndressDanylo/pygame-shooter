import pygame
import pytmx
import pytmx.util_pygame

class Map:
    def __init__(self, map_file):
        self.map_file = map_file
        self.tiles = pygame.sprite.Group()
        self.height, self.width = 0, 0

        # TODO load_pygame gives tile surfaces, if i want to get properties i'll need to use pytmx.TileMap i think.
        tmx_data = pytmx.util_pygame.load_pygame(self.map_file)
        self.width = tmx_data.width * tmx_data.tilewidth
        self.height = tmx_data.height * tmx_data.tileheight
        print("SELF", self.width/64, self.height/64)
        for layer in tmx_data.visible_layers:
            for x, y, surface in layer.tiles():
                pos_x = x * tmx_data.tilewidth - self.width // 2
                pos_y = y * tmx_data.tileheight - self.height // 2
                Tile((pos_x, pos_y), surface, self.tiles)
    
    def draw(self, surface, pos_x, pos_y):
        for sprite in self.tiles:
            rect = sprite.rect.move(pos_x, pos_y)
            surface.blit(sprite.image, rect)
        # gotta move the map :(
        #self.tiles.draw(surface)

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
