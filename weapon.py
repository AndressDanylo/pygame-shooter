import pygame
import config
from pygame.math import Vector2
from util import raycast
from math import sin, cos, acos, degrees

class Ranged:
    def __init__(self, parent):
        self.parent = parent

        self.DAMAGE = 5
        self.RANGE = 999

    def attack(self, targets):
        start = self.parent.rect.center
        direction = Vector2(cos(self.parent.angle), sin(self.parent.angle))
        result = raycast(start, start + direction * self.RANGE, targets)

        instance = result["instance"]
        if hasattr(instance, "health"):
            instance.take_damage(self.DAMAGE)
        
        return {"start": self.parent.rect.center, "end": result["position"]}

class Melee:
    def __init__(self, parent):
        self.parent = parent

        self.DAMAGE = 3
        self.REACH = 64
        self.RANGE = 90
    
    def attack(self, targets):
        direction = Vector2(cos(self.parent.angle), sin(self.parent.angle))

        for target in targets:
            target_vector = Vector2(target.rect.center) - Vector2(self.parent.rect.center)

            if target_vector.length() > self.REACH:
                continue

            if target_vector.length() > 0:
                target_vector = target_vector.normalize()

            d = direction.dot(target_vector)
            angle = degrees(acos(d))

            if abs(angle) <= self.RANGE / 2:
                target.take_damage(self.DAMAGE)

