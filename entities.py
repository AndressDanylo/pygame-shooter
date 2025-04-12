import pygame
from pygame import Vector2
import math
import config
from weapon import Ranged, Melee
from util import raycast, get_magnitude


class Entity(pygame.sprite.Sprite):
    def __init__(self, spawn_position, image_path):
        super().__init__()

        self.image = pygame.image.load(image_path).convert_alpha()
        self.original_image = self.image
        self.rect = self.image.get_rect(center=spawn_position)
        self.collision_rect = self.image.get_rect(center = spawn_position)
        # TODO get rid of magic numbers VVVVVVV
        self.collision_rect.inflate_ip(-32, -32)

        self.ranged = Ranged(self)
        self.melee = Melee(self)

        self.health = 10
        self.SPEED = 10

        self.FRICTION = 0.8
        self.velocity = pygame.math.Vector2()
        self.direction = pygame.math.Vector2()
    
    def take_damage(self, amount):
        self.health -= amount
    
    def rotate(self, image, position, target_position):
        dx, dy = target_position[0] - position[0], -(target_position[1] - position[1])
        angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(image, angle)
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))
        self.angle = math.atan2(-dy, dx)

    def move(self, position: Vector2, walls):
        """Move entity to a position """ 
        self.direction = Vector2(position) - Vector2(self.rect.center)

        if self.direction.length() > 0:
           self.direction = self.direction.normalize()

        self.velocity = (self.velocity + self.direction) * self.FRICTION
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.clamp_magnitude(self.SPEED)
        velocity = Vector2(round(self.velocity.x), round(self.velocity.y))

        collision_x, collision_y = False, False
        rect_x = self.collision_rect.move(velocity.x, 0)
        rect_y = self.collision_rect.move(0, velocity.y)
        
        for wall in walls:
            rect = getattr(wall, "collision_rect", wall.rect)
            if not collision_x and rect_x.colliderect(rect):
                collision_x = rect
                if collision_y: break
            if not collision_y and rect_y.colliderect(rect):
                collision_y = rect
                if collision_x: break

        if not collision_x:
            self.collision_rect.x += velocity.x
        else:
            if collision_x.x - rect_x.x > 0:
                self.collision_rect.right = collision_x.left
            elif collision_x.x - rect_x.x < 0:
                self.collision_rect.left = collision_x.right
        if not collision_y:
            self.collision_rect.y += velocity.y
        else:
            if collision_y.y - rect_y.y > 0:
                self.collision_rect.bottom = collision_y.top
            elif collision_y.y - rect_y.y < 0:
                self.collision_rect.top = collision_y.bottom
        self.rect.center = self.collision_rect.center



class Player(Entity):
    def __init__(self, spawn_position):
        super().__init__(spawn_position, 'assets/Player.png')

        self.ranged = Ranged(self)
        self.melee = Melee(self)

        self.SPEED = 19
        self.angle = 45
    
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

    def update(self, walls):
        self._input()
        self.rotate(self.original_image, (config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2), pygame.mouse.get_pos())
        self.velocity = (self.velocity + self.direction) * self.FRICTION
        if self.velocity.length() > 0:
            self.velocity = self.velocity.clamp_magnitude(self.SPEED)
        velocity = Vector2(round(self.velocity.x), round(self.velocity.y))

        collision_x, collision_y = False, False
        rect_x = self.collision_rect.move(velocity.x, 0)
        rect_y = self.collision_rect.move(0, velocity.y)
        # previous fixed, not sure if needed
        #rect_x.inflate_ip(0, -5)
        #rect_y.inflate_ip(-5, 0)
        
        for wall in walls:
            rect = getattr(wall, "collision_rect", wall.rect)
            if not collision_x and rect_x.colliderect(rect):
                collision_x = rect
                if collision_y: break
            if not collision_y and rect_y.colliderect(rect):
                collision_y = rect
                if collision_x: break

        if not collision_x:
            self.collision_rect.x += velocity.x
        else:
            if collision_x.x - rect_x.x > 0:
                self.collision_rect.right = collision_x.left
            elif collision_x.x - rect_x.x < 0:
                self.collision_rect.left = collision_x.right
        if not collision_y:
            self.collision_rect.y += velocity.y
        else:
            if collision_y.y - rect_y.y > 0:
                self.collision_rect.bottom = collision_y.top
            elif collision_y.y - rect_y.y < 0:
                self.collision_rect.top = collision_y.bottom
        self.rect.center = self.collision_rect.center

class Enemy(Entity):
    def __init__(self, spawn_position):
        super().__init__(spawn_position, 'assets/Monster.png')
        self.state = "idle" # changes to "chasing" when enemy spots player.
    
    def update(self, player, walls, offset):
        """Update enemy logic"""
        result = raycast(self.rect.center, player.rect.center, walls, offset)
        if result["instance"] == player:
            self.state = "chasing"
            player_position = Vector2(player.rect.centerx, player.rect.centery)
            self.rotate(self.original_image, self.rect.center, player_position) 
            self.move(player_position, walls)
            if get_magnitude(self.rect.center, player.rect.center) < 50: # TODO: replace this with a more consistent solution. 
                self.melee.attack([player]) # player is put in array because Melee.attack only accepts iterable objects. TODO: fix that.

