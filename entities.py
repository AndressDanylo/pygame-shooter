import pygame
import math

class Player:
    def __init__(self, pos_x, pos_y, speed, sprite, display_width, display_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        # TODO tweak stats
        self.velocity = pygame.Vector2()
        self.acceleration = 0.1
        self.friction = 0.8
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
        acceleration_vector = pygame.Vector2(0, 0)

        # TODO change keybinds
        if keys[pygame.K_LEFT]:
            acceleration_vector.x += self.acceleration
        if keys[pygame.K_RIGHT]:
            acceleration_vector.x -= self.acceleration
        if keys[pygame.K_UP]:
            acceleration_vector.y += self.acceleration
        if keys[pygame.K_DOWN]:
            acceleration_vector.y -= self.acceleration
        
        if acceleration_vector.length() > 0:
            acceleration_vector = acceleration_vector.normalize()

        self.velocity = (self.velocity + acceleration_vector) * self.friction
        if self.velocity.length() > 0:
            self.velocity = self.velocity.clamp_magnitude(self.speed)

        new_x = self.pos_x + self.velocity.x
        new_y = self.pos_y + self.velocity.y

        # if there is a collision on one of the axis maybe instantly stop the player ?
        collision_x, collision_y = False, False
        for tile in collidable_tiles:
            if not collision_x and self.collision_rect.colliderect(tile.rect.move(new_x, self.pos_y)):
                collision_x = True
                if collision_y: break
            if not collision_y and self.collision_rect.colliderect(tile.rect.move(self.pos_x, new_y)):
                collision_y = True
                if collision_x: break
        
        if not collision_x:
            self.pos_x = new_x
        if not collision_y:
            self.pos_y = new_y
    
    def player_rotation(self, cursor_pos, player_pos_x, player_pos_y):
        cursor_x, cursor_y = cursor_pos

        dx, dy = cursor_x - player_pos_x, cursor_y - player_pos_y
        degree = math.degrees(math.atan2(-dy, dx))
        self.actual_surf = pygame.transform.rotate(self.player_surf, degree)
        self.player_rect = self.actual_surf.get_rect(center=(self.display_width//2, self.display_height//2))

