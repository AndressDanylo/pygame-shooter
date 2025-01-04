from math import dist

def raycast(origin, end, obstructions):
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
    return {"instance": instance, "position": point}