import pygame
from pygame import Vector2
from map import Map
from entities import Player
from entities import Enemy
from weapon import Weapon
import config

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
map = Map("maps/map1.tmx")
player = Player(map.get_spawn_position())
enemies = pygame.sprite.Group()
#weapon = Weapon(10, 1000)

while running:
    spawn_monster = False

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_z:
                spawn_monster = True
            elif event.key == pygame.K_m:
                config.DEBUG = True

    player.update(map.get_collidable_tiles().sprites() + enemies.sprites())
    
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
    
    #weapon.shoot(screen)
    #weapon.melee(screen, player.hitbox_angle)

    if config.DEBUG:
        pygame.draw.rect(screen, "green", player.collision_rect.move(offset), 1)
        pygame.draw.rect(screen, "green", player.rect.move(offset), 1)

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
        
        debug_font = pygame.font.Font(None, 50)
        fps_text_surface = debug_font.render(f"FPS: {clock.get_fps() // 1}", True, "green")
        screen.blit(fps_text_surface, (20, 20))
    font = pygame.font.SysFont('Roboto', 25)
    text_surf = font.render(f"WASD - Move; ESC - Leave; M - Debug; Z - Spawn Monster (in debug)", True, "black")
    text_rect = text_surf.get_rect()
    text_rect.top = 5
    text_rect.right = config.SCREEN_WIDTH - 5
    screen.blit(text_surf, text_rect)

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
