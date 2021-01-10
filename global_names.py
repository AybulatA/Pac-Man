import pygame


#sptite groups
all_sprites = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
foods_group = pygame.sprite.Group()
energizers_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

#screen options
WIDTH, HEIGHT = 1600, 1000
FPS = 60

SPEED = 2
score = 0

CELL_SIZE = 30

CELL_SIZE_X = CELL_SIZE
CELL_SIZE_Y = CELL_SIZE

RIGHT = pygame.K_RIGHT
LEFT = pygame.K_LEFT
DOWN = pygame.K_DOWN
UP = pygame.K_UP

actions = {
    RIGHT: (0, SPEED),
    LEFT: (0, -SPEED),
    DOWN: (SPEED, 0),
    UP: (-SPEED, 0),
}


#colors
BLACK = pygame.Color('black')
FOODS_COLOR = (235, 146, 52)
