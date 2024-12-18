import pygame


class Player:
    def __init__(self, pos_x, pos_y, speed, sprite, display_width, display_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.sprite = sprite
        self.player_surf = pygame.image.load(sprite).convert_alpha()
        self.player_rect = self.player_surf.get_rect(center = (display_width//2, display_height//2))
    
    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.pos_x += self.speed
        if keys[pygame.K_RIGHT]:
            self.pos_x -= self.speed
        if keys[pygame.K_UP]:
            self.pos_y += self.speed
        if keys[pygame.K_DOWN]:
            self.pos_y -= self.speed
