import pygame
import map
from entities import Player
from weapon import Weapon
import config

# pygame setup
pygame.init()
config.SCREEN_WIDTH = pygame.display.Info().current_w
config.SCREEN_HEIGHT = pygame.display.Info().current_h
# TODO fix this? it gets strange resolution, but it does work well visually. only bugs out on my tuf laptop since it got two displays
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# player
player = Player(0, 0, 10, 'assets/Player.png')

# map
game_map = map.Map("maps/map1.tmx")

# weapon
weapon = Weapon(10, 1000)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    player.move(keys, game_map.get_collidable_tiles())

    # render
    screen.fill("gray")
    player.player_rotation(pygame.mouse.get_pos(), config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2)
    game_map.draw(screen, player.pos_x, player.pos_y)
    screen.blit(player.actual_surf, player.player_rect)
    pygame.draw.circle(screen, "red", pygame.mouse.get_pos(), 15)
    weapon.shoot(screen)
    weapon.melee(screen, player.hitbox_angle)

    if config.DEBUG:
        debug_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(debug_surface, pygame.Color(255, 0, 0, 50), player.player_rect, 1)
        pygame.draw.rect(debug_surface, "red", player.collision_rect, 1)
        screen.blit(debug_surface, debug_surface.get_rect())
    
    pygame.display.flip()

    clock.tick(config.FPS)

pygame.quit()
