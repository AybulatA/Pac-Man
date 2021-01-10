import pygame
from global_names import *
from tools import *
from generate_level import generate_level


def events():
    global running
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            player.key_pressed(event.key)


def draw_rect():
    for i in range(28):
        for j in range(31):
            pygame.draw.rect(screen, (125, 0, 0), (i * CELL_SIZE_X, j * CELL_SIZE_Y, CELL_SIZE_X, CELL_SIZE_Y), width=1)


if __name__ == '__main__':
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pac-Man')

    clock = pygame.time.Clock()
    running = True
    #start_screen(screen)
    player = generate_level(load_level('map.txt'))
    fon = pygame.transform.scale(load_image('field.jpg'), (CELL_SIZE * 28, CELL_SIZE * 31))
    while running:
        screen.blit(fon, (0, 0))
        draw_rect()
        events()
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()
