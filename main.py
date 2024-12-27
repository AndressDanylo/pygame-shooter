import pygame
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
#weapon = Weapon(10, 1000)
#enemies = pygame.sprite.Group()

while running:
    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    player.update(map.get_collidable_tiles())
    
    # render
    screen.fill("gray")
    offset = pygame.Vector2(-player.rect.x + config.SCREEN_WIDTH//2 - player.image.get_width()//2, -player.rect.y + config.SCREEN_HEIGHT//2 - player.image.get_height()//2)

    camera.center = player.rect.center
    for tile in map.get_tiles():
        if camera.colliderect(tile.rect):
            screen.blit(tile.image, tile.rect.topleft + offset)
    screen.blit(player.image, player.rect.topleft + offset)

    #for enemy in enemies:
        #enemy.draw(screen, player.pos_x, player.pos_y)
    #weapon.shoot(screen)
    #weapon.melee(screen, player.hitbox_angle)

    if config.DEBUG:
        pygame.draw.rect(screen, "red", player.collision_rect.move(offset), 1)
        pygame.draw.rect(screen, "red", player.rect.move(offset), 1)

        pygame.draw.line(screen, "black", pygame.mouse.get_pos(), (config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2))
        
        #keys = pygame.key.get_pressed()
        #if keys[pygame.K_z]:
        #    pos_x, pos_y = pygame.mouse.get_pos()
        #    pos_x -= player.pos_x
        #    pos_y -= player.pos_y
        #    enemy = Enemy(pos_x, pos_y)
        #    enemies.add(enemy)

        # debug_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        # pygame.draw.rect(debug_surface, pygame.Color(255, 0, 0, 50), player.rect, 1)
        # pygame.draw.rect(debug_surface, "red", player.collision_rect, 1)
        # screen.blit(debug_surface, debug_surface.get_rect())
        # pygame.draw.circle(screen, "red", pygame.mouse.get_pos(), 15)
        # debug_font = pygame.font.Font(None, 50)
        # fps_text_surface = debug_font.render(f"FPS: {clock.get_fps() // 1}", True, "green")
        # screen.blit(fps_text_surface, (20, 20))

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
