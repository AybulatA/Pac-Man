import pygame


#sptite groups
all_sprites = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
foods_group = pygame.sprite.Group()
energizers_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_groups = pygame.sprite.Group()


characters_obj = {
    'Pac-Man': None,
    'Blinky': None
}

game_parameters = {
    'mod': 'chase'
}

#screen options
WIDTH, HEIGHT = 1000, 1000
FPS = 60

SPEED = 2.5
score = 0

CELL_SIZE = 30

#field size, for tunnel
LEN_X = CELL_SIZE * 27

RIGHT = pygame.K_RIGHT
LEFT = pygame.K_LEFT
DOWN = pygame.K_DOWN
UP = pygame.K_UP

print('up', UP)
print('DOWN', DOWN)
print('LEFT', LEFT)
print('RIGHT', RIGHT)

VERTICAL = [RIGHT, LEFT]
HORIZONTAL = [DOWN, UP]

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

MODS_SPEED = {
    'frightened': SPEED * 0.6,
    'chase': SPEED,
    'scatter': SPEED,
    'tunnel': SPEED * 0.4
}

TUNNEL_CELLS = [[0, 14], [1, 14], [2, 14], [3, 14], [4, 14],
                [23, 14], [24, 14], [27, 14], [26, 14], [25, 14]]

BLOCK_CELLS = [[12, 11], [15, 11], [15, 23], [12, 23]]

ACTION_CELLS = [[6, 1], [21, 1], [1, 5], [6, 5], [9, 5], [12, 5], [15, 5], [18, 5], [21, 5], [26, 5], [6, 8], [21, 8],
                [6, 14], [9, 14], [18, 14], [21, 14], [9, 17], [18, 17], [6, 20], [9, 20], [18, 20], [21, 20], [6, 23],
                [9, 23], [18, 23], [12, 11], [15, 11], [15, 23], [12, 23], [21, 23], [3, 26], [24, 26],
                [12, 29], [15, 29]]

target_in_scatter_mod = {
    'Blinky': (25, 0),
    'Pinky': (2, 0),
    'Inky': (27, 31),
    'Clyde': (0, 31)
}

#colors
BLACK = pygame.Color('black')
FOODS_COLOR = (235, 146, 52)
