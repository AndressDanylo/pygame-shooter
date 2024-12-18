import pygame
import map

# pygame setup
pygame.init()
display_width = pygame.display.Info().current_w
display_height = pygame.display.Info().current_h
screen = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
running = True

# player
# TODO player class
player_surface = pygame.image.load('assets/Player.png').convert_alpha()
player_rectangle = player_surface.get_rect(center = (display_width//2, display_height//2))
player_x = 0
player_y = 0
player_speed = 10

# map
game_map = map.Map("maps/map1.tmx")

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x += player_speed
    if keys[pygame.K_RIGHT]:
        player_x -= player_speed
    if keys[pygame.K_UP]:
        player_y += player_speed
    if keys[pygame.K_DOWN]:
        player_y -= player_speed


    # render
    screen.fill("gray")
    game_map.draw(screen, player_x, player_y)
    screen.blit(player_surface, player_rectangle)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()