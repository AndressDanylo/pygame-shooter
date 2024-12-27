import pygame
from pygame import Vector2
import math
import config

class Player(pygame.sprite.Sprite):
    def __init__(self, spawn_position):
        super().__init__()

        self.direction = Vector2()
        self.velocity = Vector2()
        self.FRICTION = 0.8
        self.SPEED = 19

        self.image = pygame.image.load('assets\Player.png').convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center = spawn_position)
        self.collision_rect = self.image.get_rect(center = spawn_position)
        # TODO get rid of magic numbers VVVVVVV
        self.collision_rect.inflate_ip(-32, -32)
    
    def _input(self):
        self.direction = Vector2(0, 0)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction.x -= 1
        if keys[pygame.K_d]:
            self.direction.x += 1
        if keys[pygame.K_w]:
            self.direction.y -= 1
        if keys[pygame.K_s]:
            self.direction.y += 1
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

    def _rotate(self):
        cursor_x, cursor_y = pygame.mouse.get_pos()
        dx, dy = cursor_x - config.SCREEN_WIDTH//2, -(cursor_y - config.SCREEN_HEIGHT//2)
        angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        #self.hitbox_angle = math.degrees(math.atan2(-dy, dx))

    def update(self, collidable_tiles):
        self._input()
        self._rotate()
        self.velocity = (self.velocity + self.direction) * self.FRICTION
        if self.velocity.length() > 0:
            self.velocity = self.velocity.clamp_magnitude(self.SPEED)

        new_x = self.collision_rect.x + self.velocity.x
        new_y = self.collision_rect.y + self.velocity.y
        
        collision_x, collision_y = False, False
        rect_x = self.collision_rect.move(self.velocity.x, 0)
        rect_y = self.collision_rect.move(0, self.velocity.y)
        
        for tile in collidable_tiles:
            if not collision_x and rect_x.colliderect(tile.rect):
                collision_x = True
                if collision_y: break
            if not collision_y and rect_y.colliderect(tile.rect):
                collision_y = True
                if collision_x: break
        
        if not collision_x:
            pass
            self.collision_rect.x = new_x
            self.rect.centerx = self.collision_rect.centerx
        if not collision_y:
            pass
            self.collision_rect.y = new_y
            self.rect.centery = self.collision_rect.centery

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.surf = pygame.image.load('assets/Monster.png')
        self.rect = self.surf.get_rect(center = (self.pos_x, self.pos_y))
    
    def draw(self, surf, pos_x, pos_y):
        rect = self.rect.move(pos_x, pos_y)
        surf.blit(self.surf, rect)