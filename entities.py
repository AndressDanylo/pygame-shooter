import pygame


class Player:
    def __init__(self, pos_x, pos_y, speed, sprite, display_width, display_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.sprite = sprite
        self.player_surf = pygame.image.load(sprite)#.convert_alpha() what?
        self.player_rect = self.player_surf.get_rect(center = (display_width//2, display_height//2))
    
    def move(self, keys, collidable_tiles):
        new_x, new_y = self.pos_x, self.pos_y
        if keys[pygame.K_LEFT]:
            new_x += self.speed
        if keys[pygame.K_RIGHT]:
            new_x -= self.speed
        if keys[pygame.K_UP]:
            new_y += self.speed
        if keys[pygame.K_DOWN]:
            new_y -= self.speed
        
        collision_x, collision_y = False, False
        for tile in collidable_tiles:
            if not collision_x and self.player_rect.colliderect(tile.rect.move(new_x, self.pos_y)):
                collision_x = True
                if collision_y == True: break
            if not collision_y and self.player_rect.colliderect(tile.rect.move(self.pos_x, new_y)):
                collision_y = True
                if collision_x == True: break
        if not collision_x:
            self.pos_x = new_x
        if not collision_y:
            self.pos_y = new_y
