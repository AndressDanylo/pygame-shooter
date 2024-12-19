import pygame
import math


class Player:
    def __init__(self, pos_x, pos_y, speed, sprite, display_width, display_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed
        self.sprite = sprite
        # TODO make it obvious which surf and rect are visual and which ones are "real"
        self.player_surf = pygame.image.load(sprite)#.convert_alpha() what?
        self.player_rect = self.player_surf.get_rect(center = (display_width//2, display_height//2))
        self.collision_rect = self.player_surf.get_rect(center = (display_width//2, display_height//2))
        self.collision_rect.inflate_ip(-16, -16)
        self.display_width = display_width
        self.display_height = display_height
    
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
            if not collision_x and self.collision_rect.colliderect(tile.rect.move(new_x, self.pos_y)):
                collision_x = True
                if collision_y == True: break
            if not collision_y and self.collision_rect.colliderect(tile.rect.move(self.pos_x, new_y)):
                collision_y = True
                if collision_x == True: break
        if not collision_x:
            self.pos_x = new_x
        if not collision_y:
            self.pos_y = new_y
    
    def player_rotation(self, cursor_pos, player_pos_x, player_pos_y):
        cursor_x, cursor_y = cursor_pos

        dx, dy = cursor_x - player_pos_x, cursor_y - player_pos_y
        degree = math.degrees(math.atan2(-dy, dx))
        print(degree)
        self.actual_surf = pygame.transform.rotate(self.player_surf, degree)
        self.player_rect = self.actual_surf.get_rect(center=(self.display_width//2, self.display_height//2))

