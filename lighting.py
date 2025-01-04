import pygame
import math
import config

# def vision(surf, player, offset, tiles):
#     points = []
#     obstructions = []
#     rect = surf.get_rect().move(-offset)
#     for tile in tiles:
#         if rect.colliderect(tile.rect):
#             obstructions.append(tile)
#             pygame.draw.rect(surf, "red", tile.rect.move(offset))
    
#     for obstruction in obstructions:
#         end_point = cast_ray2(player.rect.center, obstruction.rect.topleft, obstructions)
#         points.append(end_point+offset)
#         end_point = cast_ray2(player.rect.center, obstruction.rect.topright, obstructions)
#         points.append(end_point+offset)
#         end_point = cast_ray2(player.rect.center, obstruction.rect.bottomright, obstructions)
#         points.append(end_point+offset)
#         end_point = cast_ray2(player.rect.center, obstruction.rect.bottomleft, obstructions)
#         points.append(end_point+offset)
    
#     for point in points:
#         pygame.draw.circle(surf, (255, 255, 255, 255), point, 2)

#     pygame.draw.polygon(surf, (0, 0, 0, 0), points)

# TODO made static points calculation not used, since idk how i could generate player shadows accurately
# I think i'll make only flashlight generate lights that arent pre made, cuz im not experienced enough to make this very optimised
class StaticLight(pygame.sprite.Sprite):
    def __init__(self, obstructions, position, radius = 200, color = (255, 255, 200, 55)):
        super().__init__()
        self.position = position
        self.radius = radius
        self.color = color

        self.rect = pygame.Rect(position.x-radius, position.y-radius, radius*2, radius*2)
        self.image = pygame.image.load('assets\Light.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        self.obstructions = self._get_obstructions(obstructions)
        self.points = self._get_points(self.obstructions)

        self.light_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.shadow_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
    
    def update(self, surf, offset, entities):
        if config.DEBUG:
            for object in self.obstructions:
                pygame.draw.rect(surf, (255, 0, 255, 50), object.rect.move(offset), 0)
            pygame.draw.circle(surf, (255, 0, 255, 150), self.position + offset, self.radius, 1)
            for point in self.points:
                pygame.draw.circle(surf, (255, 255, 255, 255), point + offset, 3)
        
        # points = []
        global_points = []
        # for point in self.points:
        #     points.append(point - self.position + (self.rect.width//2, self.rect.height//2))
        #     global_points.append(point + offset)
        points = []
        for point in self._get_dynamic_points(entities + self.obstructions):
            points.append(point - self.position + (self.rect.width//2, self.rect.height//2))
            global_points.append(point + offset)
            
        self.light_surface.fill((0, 0, 0, 0))
        self.shadow_surface.fill((0, 0, 0, 0))

        self.light_surface.blit(self.image, (0, 0))
        if len(points) > 2:
            pygame.draw.polygon(self.shadow_surface, (255, 255, 255, 255), points)
            self.light_surface.blit(self.shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        # if len(dynamic_points) > 2:
        #     self.shadow_surface.fill((0, 0, 0, 0))
        #     pygame.draw.polygon(self.shadow_surface, (255, 255, 255, 255), dynamic_points)
        #     self.light_surface.blit(self.shadow_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

        pygame.draw.polygon(surf, (0, 0, 0, 0), global_points)
        surf.blit(self.light_surface, self.rect.topleft + offset)
    
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
                point = _raycast(self.position, self.position + direction * self.radius, obstructions)
                points.append(point)
        points.sort(key=lambda p: math.atan2(p[1] - self.position[1], p[0] - self.position[0]))
        return points

    def _get_dynamic_points(self, entities):
        points = []
        for object in entities:
            rect = getattr(object, "collision_rect", object.rect)
            for corner in (rect.topright, rect.topleft, rect.bottomright, rect.bottomleft):
                direction = pygame.math.Vector2(corner[0] - self.position[0], corner[1] - self.position[1])
                if direction.length() > 0:
                    direction = direction.normalize()
                point = _raycast(self.position, self.position + direction * self.radius, entities)
                points.append(point)
        points.sort(key=lambda p: math.atan2(p[1] - self.position[1], p[0] - self.position[0]))
        return points

def _raycast(origin, end, obstructions):
    point = end
    min_distance = math.dist(origin, end)

    for object in obstructions:
        rect = getattr(object, "collision_rect", object.rect)
        intersection = rect.clipline(origin, end)
        if intersection:
            intersection_point = intersection[0]
            distance = math.dist(origin, intersection_point)
            if distance < min_distance:
                min_distance = distance
                point = intersection_point
    return point

# def draw_lighting(player, walls, max_distance=300, cone_angle=45, offset=(0, 0)):
#     screen = pygame.display.get_surface()

#     # Flashlight parameters
#     num_rays = 25
#     angle_step = math.radians(cone_angle) / num_rays
#     base_angle = math.radians(player.angle) + math.radians(cone_angle) / 2

#     light_points = [player.rect.center+offset]  # Start point of the cone

#     # Cast rays
#     for i in range(num_rays + 1):
#         ray_angle = -base_angle + i * angle_step
#         end_point = cast_ray(player.rect.center, ray_angle, walls, max_distance)
#         light_points.append(end_point+offset)

#     if len(light_points) > 2:
#         pygame.draw.polygon(surf, (0, 0, 0, 0), light_points)
#     pygame.draw.circle(surf, (0, 0, 0, 0), player.rect.center+offset, 35)

#     # # Blend the light surface with the display
#     