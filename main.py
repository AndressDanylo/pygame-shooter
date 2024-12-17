import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

# player
player_surface = pygame.image.load('assets/Player.png').convert_alpha()
player_rectangle = player_surface.get_rect(topleft = (0, 0))


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("gray")
    screen.blit(player_surface, player_rectangle)

    # RENDER YOUR GAME HERE


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()