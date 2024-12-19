import pygame
import map
from entities import Player

# pygame setup
pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((display_width, display_height) )
clock = pygame.time.Clock()
running = True

# player
player = Player(0, 0, 10, 'assets/Player.png', display_width, display_height)

# map
game_map = map.Map("maps/map1.tmx", display_width, display_height)

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    player.move(keys, game_map.get_collidable_tiles())

    # render
    screen.fill("gray")
    player.player_rotation(pygame.mouse.get_pos(), display_width//2, display_height//2)
    game_map.draw(screen, player.pos_x, player.pos_y)
    screen.blit(player.actual_surf, player.player_rect)
    pygame.draw.circle(screen, "red", pygame.mouse.get_pos(), 15)
    #pygame.draw.rect(screen, "red", player.collision_rect, 1)
    
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
