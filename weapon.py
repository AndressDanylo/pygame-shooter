import pygame
import config
from pygame.math import Vector2
from util import raycast
from math import radians, sin, cos

class Ranged:
    def __init__(self, parent):
        self.parent = parent

        self.DAMAGE = 5
        self.RANGE = 999

    def attack(self, targets):
        start = self.parent.rect.center
        direction = pygame.math.Vector2(cos(self.parent.angle), sin(self.parent.angle))
        result = raycast(start, start + direction * self.RANGE, targets)

        instance = result["instance"]
        if hasattr(instance, "health"):
            instance.take_damage(self.DAMAGE)
        
        return {"start": self.parent.rect.center, "end": result["position"]}

# TODO rework this into melee
class Weapon:
    def __init__(self, damage, bullet_range):
        self.damage = damage
        self.bullet_range = bullet_range
        self.player_pos_x = config.SCREEN_WIDTH // 2
        self.player_pos_y = config.SCREEN_HEIGHT // 2
        self.player_position = (self.player_pos_x, self.player_pos_y)
    
    def get_shoot_direction(self):
        cursor_position_vector = Vector2(pygame.mouse.get_pos())
        self.player_position_vector = Vector2(self.player_position)
        difference_vector = cursor_position_vector - self.player_position_vector
        return difference_vector.normalize() if difference_vector.length() > 0 else Vector2(0, 0)

    def shoot(self, surface):
        if pygame.mouse.get_pressed()[0]:
            shoot_direction = self.get_shoot_direction()
            endpoint = self.player_position_vector + shoot_direction * self.bullet_range
            pygame.draw.line(surface, "red", self.player_position, endpoint)
    
    def get_melee_hitbox(self, hitbox_angle, distance=30):
        # get melee hitbox position and rotation
        rad_angle = radians(hitbox_angle)
        # distance variable represents distance between player and the hitbox
        hitbox_x = self.player_pos_x + distance * cos(rad_angle)
        hitbox_y = self.player_pos_y - distance * sin(rad_angle)
        return Vector2(hitbox_x, hitbox_y)


    def melee(self, surface, hitbox_angle):
        if pygame.mouse.get_pressed()[0]:
            self.hitbox_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
            self.hitbox_surf.fill((255, 0, 0, 128))
            hitbox_position = self.get_melee_hitbox(hitbox_angle)
            rotated_hitbox = pygame.transform.rotate(self.hitbox_surf, hitbox_angle)
            surface.blit(rotated_hitbox, rotated_hitbox.get_rect(center=hitbox_position))
