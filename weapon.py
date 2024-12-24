import pygame
from pygame.math import Vector2
from math import radians, sin, cos


class Weapon:
    def __init__(self, damage, bullet_range, display_width, display_height):
        self.damage = damage
        self.bullet_range = bullet_range
        self.display_width = display_width
        self.display_height = display_height

    def shoot(self, surface):
        if pygame.mouse.get_pressed()[0]:
            cursor_position = Vector2(pygame.mouse.get_pos())
            player_position = Vector2((self.display_width//2, self.display_height//2))
            shoot_direction = (cursor_position - player_position).normalize()
            endpoint = player_position + shoot_direction * self.bullet_range
            pygame.draw.line(surface, "red", (self.display_width//2, self.display_height//2), endpoint)

    def melee(self, hitbox_angle):
        self.hitbox_surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.hitbox_surf.fill((255, 0, 0, 128))
        rad_angle = radians(hitbox_angle)
        self.hitbox_x = self.display_width//2 + 30 * cos(rad_angle)
        self.hitbox_y = self.display_height//2 - 30 * sin(rad_angle)
        self.rotated_hitbox = pygame.transform.rotate(self.hitbox_surf, hitbox_angle)
