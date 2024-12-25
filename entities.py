import pygame
import math
import config

class Player:
    def __init__(self, pos_x, pos_y, speed, sprite):
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        # TODO tweak stats
        self.velocity = pygame.Vector2()
        self.acceleration = 0.0001
        self.friction = 0.8
        self.speed = speed

        self.center_x = config.SCREEN_WIDTH // 2
        self.center_y = config.SCREEN_HEIGHT // 2

        self.sprite = sprite
        # TODO make it obvious which surf and rect are visual and which ones are "real"
        self.player_surf = pygame.image.load(sprite).convert_alpha()
        self.player_rect = self.player_surf.get_rect(center = (self.center_x, self.center_y))
        self.collision_rect = self.player_surf.get_rect(center = (self.center_x, self.center_y))
        self.collision_rect.inflate_ip(-32, -32)
    
    def move(self, keys, collidable_tiles):
        acceleration_vector = pygame.Vector2(0, 0)

        # TODO change keybinds
        if keys[pygame.K_a]:
            acceleration_vector.x += self.acceleration
        if keys[pygame.K_d]:
            acceleration_vector.x -= self.acceleration
        if keys[pygame.K_w]:
            acceleration_vector.y += self.acceleration
        if keys[pygame.K_s]:
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
        self.player_rect = self.actual_surf.get_rect(center=(self.center_x, self.center_y))
        self.hitbox_angle = math.degrees(math.atan2(-dy, dx))
