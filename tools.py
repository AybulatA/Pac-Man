import os
import sys
from global_names import *
from random import choice
import pygame


def load_image(name, colorkey=None, key_path=None):
    path = 'data'
    if key_path is not None:
        path += '/' + key_path
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, encoding='utf-8') as mapFile:
        return [line for line in mapFile]


def terminate():
    pygame.quit()
    sys.exit()


def start_screen(screen):
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()


def load_pacman_sprites(sprites):
    sprites_pac = {'alive': sprites['chase'].copy(),
                   'dead': [],
                   'start_image': [load_image('start.png', key_path='Pac-Man')]
                   }

    sprites_pac['alive'][UP].extend(sprites_pac['start_image'])
    sprites_pac['alive'][RIGHT].extend(sprites_pac['start_image'])

    sprites_pac['alive'][UP].reverse()
    sprites_pac['alive'][RIGHT].reverse()

    for sprite in sprites_pac['alive'][UP]:
        sprites_pac['alive'][DOWN].append(pygame.transform.flip(sprite, False, True))

    for sprite in sprites_pac['alive'][RIGHT]:
        sprites_pac['alive'][LEFT].append(pygame.transform.flip(sprite, True, False))

    for i in range(1, 12):
        n = 'dead_' + str(i) + '.png'
        im = load_image(n, key_path='Pac-Man')
        im = pygame.transform.scale(im, (int(CELL_SIZE * 1.5),
                                         int(CELL_SIZE * 1.5)))
        sprites_pac['dead'].append(im)

    return sprites_pac


def load_and_resize_sprites(name):
    sprites = {
        'chase': {
            UP: [load_image('up(first).png', key_path=name),
                 load_image('up(second).png', key_path=name)],
            RIGHT: [load_image('right(first).png', key_path=name),
                    load_image('right(second).png', key_path=name)],
            DOWN: [],
            LEFT: []
        },
        'dead': []
    }
    if name == 'Pac-Man':
        sprites = load_pacman_sprites(sprites)
    else:
        f = [load_image('frightened(first).png', key_path='Ghost'),
             load_image('frightened(second).png', key_path='Ghost')]
        sprites['frightened'] = f.copy()

        f.append(load_image('half_frightened(first).png', key_path='Ghost'))
        f.append(load_image('half_frightened(second).png', key_path='Ghost'))

        sprites['half_frightened'] = f.copy()

        sprites['chase'][DOWN] = [load_image('down(first).png', key_path=name),
                                  load_image('down(second).png', key_path=name)]

        sprites['chase'][LEFT] = [load_image('left(first).png', key_path=name),
                                  load_image('left(second).png', key_path=name)]

        sprites['scatter'] = sprites['chase'].copy()

        sprites['points'] = []
        p = ['200', '400', '800', '1600']
        for i in p:
            sprites['points'].append(load_image(i + '.png', key_path='Ghost'))

        sprites['dead'] = {
            UP: [load_image('dead(up).png', key_path='Ghost')],
            DOWN: [load_image('dead(down).png', key_path='Ghost')],
            RIGHT: [load_image('dead(right).png', key_path='Ghost')],
            LEFT: [load_image('dead(left).png', key_path='Ghost')]
        }

    return resize(sprites)


def resize(sprites):
    for i in sprites:
        try:
            for j in sprites[i]:
                for z in range(len(sprites[i][j])):
                    sprites[i][j][z] = pygame.transform.scale(sprites[i][j][z],
                                                              (int(CELL_SIZE * 1.5),
                                                               int(CELL_SIZE * 1.5)))
                    sprites[i][j][z].set_colorkey(BLACK)
        except Exception:
            for j in range(len(sprites[i])):
                sprites[i][j] = pygame.transform.scale(sprites[i][j],
                                                       (int(CELL_SIZE * 1.5),
                                                        int(CELL_SIZE * 1.5)))
                sprites[i][j].set_colorkey(BLACK)

    return sprites


def random(keys):
    return choice(keys)


def possible_keys(obj, point=None):
    ans = list()

    pos_x, pos_y = position(obj)

    x_t, y_t = cell_center(obj)

    if x_t != MIDDLE or y_t != MIDDLE:
        return [obj.action]

    acts = {
        RIGHT: (pos_x + 1, pos_y),
        LEFT: (pos_x - 1, pos_y),
        DOWN: (pos_x, pos_y + 1),
        UP: (pos_x, pos_y - 1)
    }

    points = ['.', ' ', '0']
    if point is not None:
        points.append(point)

    for key, value in acts.items():
        x_cell = value[0] % LEN_X
        y_cell = value[1]
        if game_parameters['map'][y_cell][x_cell] in points:
            ans.append(key)
    return ans


def position(obj):
    return [int((obj.rect.x + CELL_SIZE // 4 + CELL_SIZE * 1.5 / 2) / CELL_SIZE),
            int((obj.rect.y + CELL_SIZE // 4 + CELL_SIZE * 1.5 / 2) / CELL_SIZE)]


def cell_center(obj):
    return ((obj.real_rect_x + CELL_SIZE // 4 + CELL_SIZE * 1.5 / 2) % CELL_SIZE,
            (obj.real_rect_y + CELL_SIZE // 4 + CELL_SIZE * 1.5 / 2) % CELL_SIZE)


def kill_all_sprites():
    n = len(attempts_group)
    for i in all_sprites:
        if i in player_group or i in enemy_group or n == 0:
            i.kill()
    if n != 0:
        for i in attempts_group:
            if n == 1:
                i.kill()
            n -= 1
        game_parameters['mod'] = 'attempt'
    else:
        game_parameters['score'] = 0
        game_parameters['level'] = 1

        game_parameters['mod'] = 'game over'


def change_way():
    for i in enemy_group:
        i.action = opposite_keys[i.action]


#in frightened mod timer stops
def stop_timer():
    game_parameters['stopped timer'] = pygame.time.get_ticks()
    time = 6000 / 19 * (19 - game_parameters['level'])
    pygame.time.set_timer(FRIGHTENED_EVENT_ID, int(time), True)
    pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, int(time) + 2000, True)
