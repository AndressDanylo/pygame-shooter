import pygame
from math import dist
from config import DEBUG, SCREEN_HEIGHT, SCREEN_WIDTH
from pygame import Vector2

def raycast(origin, end, obstructions, offset = Vector2(0, 0)):
    instance = None
    point = end
    min_distance = dist(origin, end)

    for object in obstructions:
        rect = getattr(object, "collision_rect", object.rect)
        intersection = rect.clipline(origin, end)
        if intersection:
            intersection_point = intersection[0]
            distance = dist(origin, intersection_point)
            if distance < min_distance:
                min_distance = distance
                point = intersection_point
                instance = object
    
    if DEBUG == True and offset:
        screen_origin = origin + offset
        screen_end = end + offset
        screen_point = point + offset
        surface = pygame.display.get_surface()
        pygame.draw.line(surface, (50, 0, 0), screen_origin, screen_end, 1)
        pygame.draw.line(surface, (255, 0, 0), screen_origin, screen_point, 1)
    return {"instance": instance, "position": point}

def normalize_angle(angle):
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle