import pygame
import map
from entities import Player

# pygame setup
pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

# player
player = Player(0, 0, 10, 'assets/Player.png', display_width, display_height)

# map
game_map = map.Map("maps/map1.tmx")

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    player.move(keys)
    


    # render
    screen.fill("gray")
    game_map.draw(screen, player.pos_x, player.pos_y)
    screen.blit(player.player_surf, player.player_rect)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
