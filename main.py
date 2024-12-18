import pygame
import map

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# player
# TODO player class
player_surface = pygame.image.load('assets/Player.png').convert_alpha()
player_rectangle = player_surface.get_rect(center = (1280//2, 720//2))
player_x = 0
player_y = 0

# map
game_map = map.Map("maps\map1.tmx")

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # TODO hold input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x += 10
            if event.key == pygame.K_RIGHT:
                player_x -= 10
            if event.key == pygame.K_UP:
                player_y += 10
            if event.key == pygame.K_DOWN:
                player_y -= 10

    # render
    screen.fill("gray")
    game_map.draw(screen, player_x, player_y)
    screen.blit(player_surface, player_rectangle)

    pygame.display.flip()

    # 
    clock.tick(60)

pygame.quit()