import pygame


#sptite groups
all_sprites = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
foods_group = pygame.sprite.Group()
energizers_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_groups = pygame.sprite.Group()

#screen options
WIDTH, HEIGHT = 1600, 1000
FPS = 60

SPEED = 3
score = 0

CELL_SIZE = 30

#field size, for tunnel
LEN_X = CELL_SIZE * 27

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

opposite_keys = {
    RIGHT: LEFT,
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT
}

#colors
BLACK = pygame.Color('black')
FOODS_COLOR = (235, 146, 52)
