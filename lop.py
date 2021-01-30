import sys
import pygame
import os


def load_image(name, colorkey=None, key_path=None):
    colorkey = -1
    path = 'data'
    if key_path is not None:
        path += '/' + key_path
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    #if colorkey is not None:
    #    if colorkey == -1:
    #        colorkey = image.get_at((0, 0))
    #    image.set_colorkey(colorkey)
    #else:
    #    image = image.convert_alpha()
    return image


CELL_SIZE = 16


def draw_rect():
    for i in range(14):
        for j in range(10):
            pygame.draw.rect(screen, (125, 0, 0), (3 + i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE), width=1)


if __name__ == '__main__':
    pygame.init()
    size = 227, 160
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Pac-Man')

    font = pygame.font.SysFont("Arial", 18)

    clock = pygame.time.Clock()
    running = True
    fon = load_image('data.png')
    while running:
        screen.fill((255, 255, 255))
        screen.blit(fon, (0, 0))
        draw_rect()
        pygame.display.flip()
    pygame.quit()
