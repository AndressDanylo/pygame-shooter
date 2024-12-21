import pygame
from pygame.math import Vector2


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
