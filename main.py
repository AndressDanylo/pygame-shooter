import pygame
from pygame import Vector2
import config
import random
from math import cos, sin

from map import Map
from entities import Player, Enemy
from lighting import StaticLight, FlashLight

# pygame setup
pygame.init()

config.SCREEN_WIDTH = pygame.display.Info().current_w
config.SCREEN_HEIGHT = pygame.display.Info().current_h
config.SCALE = min(config.SCREEN_WIDTH / config.VIRTUAL_WIDTH, config.SCREEN_HEIGHT / config.VIRTUAL_HEIGHT)

screen_mode = 0 if config.DEBUG else pygame.FULLSCREEN
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), screen_mode)
camera = screen.get_rect()
if config.DEBUG:
    camera.inflate_ip(-64, -64)

clock = pygame.time.Clock()
running = True

# objects
enemies = pygame.sprite.Group()
lights = pygame.sprite.Group()
lines = []
map = Map("maps/map1.tmx", enemies)
player = Player(map.get_spawn_position())

# w, h = screen.get_width(), screen.get_height()
# for i in range(1, 10):
#     light = StaticLight(map.get_collidable_tiles(), (random.randint(-w, w), random.randint(-h, h))+map.get_spawn_position())
#     #lights.add(light)
# light = StaticLight(map.get_collidable_tiles(), map.get_spawn_position())
# lights.add(light)

#flashlight = FlashLight(player, map.get_collidable_tiles(), map.get_spawn_position(), 400)

while running:
    spawn_monster = False
    ranged_attack = False
    melee_attack = False

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                ranged_attack = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                melee_attack = True
            elif event.key == pygame.K_z: # debug stuff
                spawn_monster = True
            elif event.key == pygame.K_m:
                config.DEBUG = not config.DEBUG

    # logic
    player.update(map.get_collidable_tiles().sprites() + enemies.sprites())

    if ranged_attack:
        line = player.ranged.attack(enemies.sprites() + map.get_collidable_tiles().sprites())
        if line:
            lines.append(line)
    if melee_attack:
        player.melee.attack(enemies)
    
    for enemy in enemies:
        if enemy.health <= 0:
            enemies.remove(enemy)
            del enemy

    # render
    screen.fill("gray")
    offset = pygame.Vector2(-player.rect.x + config.SCREEN_WIDTH//2 - player.image.get_width()//2, -player.rect.y + config.SCREEN_HEIGHT//2 - player.image.get_height()//2)
    camera.center = player.rect.center
    
    for tile in map.get_tiles():
        if camera.colliderect(tile.rect):
            screen.blit(tile.image, tile.rect.topleft + offset)
    
    screen.blit(player.image, player.rect.topleft + offset)
    for enemy in enemies:
        if camera.colliderect(enemy.rect):
            screen.blit(enemy.image, enemy.rect.topleft + offset)

    entities = enemies.sprites()
    entities.append(player)

    # flashlight.move()

    # lighting_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    # lighting_surf.fill((0, 0, 0, 150))
    # lights.update(lighting_surf, offset)
    # flashlight.update(lighting_surf, offset)
    # screen.blit(lighting_surf, (0, 0))

    for line in lines:
        pygame.draw.line(screen, (255, 255, 0), line["start"] + offset, line["end"] + offset, 1)
    lines.clear()

    # vision_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    # vision_surf.fill((0, 0, 0, 252))
    # lighting.vision(vision_surf, player, offset, map.get_collidable_tiles())
    # screen.blit(vision_surf, (0, 0))

    if config.DEBUG:
        pygame.draw.rect(screen, "green", player.collision_rect.move(offset), 1)
        pygame.draw.rect(screen, "green", player.rect.move(offset), 1)

        pygame.draw.circle(screen, (255, 0, 255), player.rect.center + offset, player.melee.REACH, 1)
        direction = Vector2(cos(player.angle), sin(player.angle))
        left_direction = direction.rotate(-player.melee.RANGE / 2)
        right_direction = direction.rotate(player.melee.RANGE / 2)
        center = player.rect.center + offset
        pygame.draw.line(screen, (255, 0, 255), center, center + left_direction * player.melee.REACH, 1)
        pygame.draw.line(screen, (255, 0, 255), center, center + right_direction * player.melee.REACH, 1)

        pygame.draw.line(screen, "black", pygame.mouse.get_pos(), (config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2))

        if spawn_monster:
            position = pygame.mouse.get_pos()
            position = Vector2(position[0], position[1])
            position -= offset
            enemy = Enemy(position)
            enemies.add(enemy)
        for enemy in enemies:
            pygame.draw.rect(screen, "red", enemy.rect.move(offset), 1)
            pygame.draw.rect(screen, "red", enemy.collision_rect.move(offset), 1)
            # TODO: change the onscreen enemies handling
            if camera.colliderect(enemy.rect):
                enemy.update((player.rect.x, player.rect.y), map.get_collidable_tiles().sprites())
        
        debug_font = pygame.font.Font(None, 50)
        fps_text_surface = debug_font.render(f"FPS: {clock.get_fps() // 1}", True, "green")
        screen.blit(fps_text_surface, (20, 20))

    font = pygame.font.SysFont('Roboto', 25)
    text_surf = font.render(f"WASD - Move; M1 - Shoot; Space - Melee; ESC - Leave; M - Debug; Z - Spawn Monster (in debug)", True, "black")
    text_rect = text_surf.get_rect()
    text_rect.top = 5
    text_rect.right = config.SCREEN_WIDTH - 5
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
