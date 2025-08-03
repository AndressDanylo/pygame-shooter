import pygame
import math
import config
from pygame.math import Vector2
from util import raycast, normalize_angle
from math import sin, cos
class Light(pygame.sprite.Sprite):
    def __init__(self, position, radius=200, color=(255, 255, 200, 55)):
        super().__init__()
        self.position = pygame.math.Vector2(position)
        self.radius = radius
        self.color = color

        self.rect = pygame.Rect(position[0] - radius, position[1] - radius, radius * 2, radius * 2)
        self.image = pygame.image.load('assets/Light.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        self.light_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)

    def _update_light(self, points):
        self.light_surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))
        self.light_surface.blit(self.image, (0, 0))

        if len(points) > 2:
            pygame.draw.polygon(self.shadow_surface, (255, 255, 255, 255), points)
            self.light_surface.blit(self.shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

    def _draw_debug(self, surf, offset, points, obstructions):
        for object in obstructions:
            pygame.draw.rect(surf, (255, 0, 255, 50), object.rect.move(offset), 0)
        pygame.draw.circle(surf, (255, 0, 255, 150), self.position + offset, self.radius, 1)
        for point in points:
            pygame.draw.circle(surf, (255, 255, 255, 255), point + offset, 3)
    
    def _get_obstructions(self, obstructions):
        result = []
        for object in obstructions:
            # TODO better way of getting obsturctions, cuz rn u still get some excess
            if self.rect.colliderect(getattr(object, "collision_rect", object.rect)):
                result.append(object)
        return result

    def _get_points(self, obstructions):
        points = []
        for object in obstructions:
            for corner in (object.rect.topright, object.rect.topleft, object.rect.bottomright, object.rect.bottomleft):
                direction = pygame.math.Vector2(corner[0] - self.position[0], corner[1] - self.position[1])
                if direction.length() > 0:
                    direction = direction.normalize()
                result = raycast(self.position, self.position + direction * self.radius, obstructions)
                points.append(result["position"])
        points.sort(key=lambda p: math.atan2(p[1] - self.position[1], p[0] - self.position[0]))
        return points

class StaticLight(Light):
    def __init__(self, obstructions, position, radius = 200, color = (255, 255, 200, 55)):
        super().__init__(position, radius, color)

        self.obstructions_og = obstructions
        self.obstructions = self._get_obstructions(obstructions)
        self.points = self._get_points(self.obstructions)

        self.cached_polygon = None
        self.cached_light_surface = None

        points = []
        global_points = []
        for point in self.points:
            points.append(point - self.position + (self.rect.width // 2, self.rect.height // 2))
            global_points.append(point)
        self._update_light(points)

        if len(global_points) > 2:
            self.cached_polygon = global_points
            self.cached_light_surface = self.light_surface.copy()
    
    def update(self, surf, offset, camera):
        if config.DEBUG:
            self._draw_debug(surf, offset, self.points, self.obstructions)

        if self.rect.colliderect(camera):
            if self.cached_polygon and self.cached_light_surface:
                offset_polygon = [p + offset for p in self.cached_polygon]
                pygame.draw.polygon(surf, (0, 0, 0, 0), offset_polygon)
                surf.blit(self.cached_light_surface, self.rect.topleft + offset)
    
    # def update(self, surf, offset):
    #     if config.DEBUG:
    #         self._draw_debug(surf, offset, self.points, self.obstructions)
        
    #     points = []
    #     global_points = []
    #     for point in self.points:
    #         points.append(point - self.position + (self.rect.width//2, self.rect.height//2))
    #         global_points.append(point + offset)
        
    #     self._update_light(points)
    #     if len(global_points) > 2:
    #         pygame.draw.polygon(surf, (0, 0, 0, 0), global_points)
    #         surf.blit(self.light_surface, self.rect.topleft + offset)

class FlashLight(Light):
    def __init__(self, parent, obstructions, position, radius = 200, color = (255, 255, 200, 55)):
        super().__init__(position, radius, color)

        self.angle = 90
        self.direction = Vector2(1, 0)

        self.parent = parent
        self.obstructions_og = obstructions
        self.obstructions = self._get_obstructions(obstructions)
        self.points = self._get_points(self.obstructions)

    def _get_obstructions(self, obstructions):
        relevant_obstructions = []
        for obj in obstructions:
            obj_center = pygame.math.Vector2(obj.rect.center)
            direction_to_obj = obj_center - self.position
            if direction_to_obj.length() > self.radius:
                continue

            angle_to_obj = normalize_angle(self.direction.angle_to(direction_to_obj))

            if abs(angle_to_obj) <= self.angle / 2:
                relevant_obstructions.append(obj)

        return relevant_obstructions

    def update(self, surf, offset):
        if config.DEBUG:
            self._draw_debug(surf, offset, self.points, self.obstructions)

        points = []
        global_points = []
        for point in self.points:
            direction_to_point = Vector2(point - self.position).normalize()
            angle_to_point = self.direction.angle_to(direction_to_point)
            if abs(angle_to_point) <= self.angle / 2:
                points.append(point - self.position + (self.rect.width // 2, self.rect.height // 2))
                global_points.append(point + offset)
        
        center_point = self.position
        points.insert(0, center_point - self.position + (self.rect.width // 2, self.rect.height // 2))
        global_points.insert(0, center_point + offset)

        self._update_light(points)
        pygame.draw.polygon(surf, (0, 0, 0, 0), global_points)
        surf.blit(self.light_surface, self.rect.topleft + offset)

    def move(self):
        position = self.parent.rect.center
        self.position = Vector2(position[0], position[1])
        self.rect.center = position
        self.direction = Vector2(cos(self.parent.angle), sin(self.parent.angle))
        self.obstructions = self._get_obstructions(self.obstructions_og)
        self.points = self._get_points(self.obstructions)
    
    def _draw_debug(self, surf, offset, points, obstructions):
        for obj in obstructions:
            pygame.draw.rect(surf, (255, 0, 255, 50), obj.rect.move(offset), 0)
        pygame.draw.circle(surf, (255, 0, 255, 150), self.position + offset, self.radius, 1)
        for point in points:
            pygame.draw.circle(surf, (255, 255, 255, 255), point + offset, 3)

        # Draw flashlight cone
        end_left = self.position + self.direction.rotate(-self.angle / 2) * self.radius
        end_right = self.position + self.direction.rotate(self.angle / 2) * self.radius
        pygame.draw.line(surf, (0, 255, 0), self.position + offset, end_left + offset, 1)
        pygame.draw.line(surf, (0, 255, 0), self.position + offset, end_right + offset, 1)

    def _update_light(self, points):
        self.light_surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))

        self.light_surface.blit(self.image, (0, 0))
        if len(points) > 2:
            pygame.draw.polygon(self.shadow_surface, (255, 255, 255, 255), points)
            self.light_surface.blit(self.shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)