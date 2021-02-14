import pygame


#sptite groups
all_sprites = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
foods_group = pygame.sprite.Group()
energizers_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
attempts_group = pygame.sprite.Group()


game_obj = {
    'Pac-Man': None,
    'Blinky': None,
    'Border': None
}

#game mods
FRIGHTENED = 'frightened'
H_FRIGHTENED = 'half_frightened'
CHASE = 'chase'
SCATTER = 'scatter'
GAME_OVER = 'game over'
ROUND_OVER = 'round over'
ATTEMPT = 'attempt'
STOP = 'stop'
DEAD = 'dead'


game_parameters = {
    'mod': SCATTER,
    'level': 1,
    'timer_num': 0,
    'ate ghosts': -1,
    'stopped timer': 0,
    'saved mod': None,
    'map': None,
    'score': 0,
    'score per round': 0
}

#screen options
WIDTH, HEIGHT = 1000, 1000
FPS = 60

SPEED = 2.5

DEFAULT_EVENT_ID = pygame.USEREVENT + 1
FRIGHTENED_EVENT_ID = pygame.USEREVENT + 2
HALF_FRIGHTENED_EVENT_ID = pygame.USEREVENT + 3

CELL_SIZE = 30

#sprite middle
MIDDLE = CELL_SIZE * 1.5 / 2

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
    'tunnel': SPEED * 0.4,
    'dead': SPEED * 3
}

TUNNEL_CELLS = [[0, 14], [1, 14], [2, 14], [3, 14], [4, 14],
                [23, 14], [24, 14], [27, 14], [26, 14], [25, 14]]

BLOCK_CELLS = [[12, 11], [15, 11], [15, 23], [12, 23]]

HOME_TAR = [13, 15]
h = [[i, 13] for i in range(11, 17)]
h.extend([[i, 14] for i in range(11, 17)])
h.extend([[i, 15] for i in range(11, 17)])
HOME = h.copy()
h.extend([[13, 12], [14, 12]])
HOME_WITH_DOORS = h.copy()

target_in_scatter_mod = {
    'Blinky': (25, 0),
    'Pinky': (2, 0),
    'Inky': (27, 31),
    'Clyde': (0, 31)
}

LEVEL_TIME_CHANGE = {
    '1': [7, 20, 7, 20, 5, 20, 5],
    '2 3 4 5': [7, 20, 7, 20, 5, 1033, 1 / 60],
    'infinity': [5, 20, 5, 20, 5, 1037, 1 / 60]
}

#colors
BLACK = pygame.Color('black')
FOODS_COLOR = (235, 146, 52)
