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
    return image


def load_music(name, key_path=None):
    path = 'data'
    if key_path is not None:
        path += '/' + key_path
    path += '/music'
    fullname = os.path.join(path, name)
    if not os.path.isfile(fullname):
        print(f"Файл'{fullname}' не найден")
        sys.exit()
    return pygame.mixer.Sound(fullname)


def load_sprites():
    names = ['Blinky', 'Pinky', 'Clyde', 'Inky', 'Pac-Man']
    for name in names:
        SPRITES[name] = load_and_resize_sprites(name)
    SPRITES['Border'] = load_image('field.jpg', colorkey=BLACK)

    im = load_image('right(first).png', key_path='Pac-Man')
    SPRITES['Attempts'] = pygame.transform.flip(im, True, False)

    SPRITES['stop'] = load_image('stop.jpg', key_path='game', colorkey=WHITE)
    SPRITES['sound_on'] = pygame.transform.scale(load_image('sound_on.png', key_path='game', colorkey=WHITE), (CELL_SIZE * 2, CELL_SIZE * 2))
    SPRITES['sound_on'].set_colorkey(WHITE)

    SPRITES['sound_off'] = pygame.transform.scale(load_image('sound_off.png',
                                                             key_path='game', colorkey=WHITE),
                                                  (CELL_SIZE * 2, CELL_SIZE * 2))
    SPRITES['sound_off'].set_colorkey(WHITE)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, encoding='utf-8') as mapFile:
        return [line for line in mapFile]


def terminate():
    pygame.quit()
    sys.exit()


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
    for obj in all_sprites:
        obj.kill()


def kill_attempt_and_reset_game():
    n = len(attempts_group)
    for i in all_sprites:
        if i in player_group or i in enemy_group or n == 0:
            i.kill()
    if n != 0:
        for i in attempts_group:
            if n == 1:
                i.kill()
            n -= 1
        game_parameters['mod'] = ATTEMPT
    else:
        game_parameters['score'] = 0
        game_parameters['level'] = 1

        game_parameters['mod'] = GAME_OVER


def change_way():
    for ghost in enemy_group:
        if ghost.alive and ghost.at_home is False and ghost.frightened is False:
            ghost.action = opposite_keys[ghost.action]


def change_frightened(b):
    for i in enemy_group:
        if i.newborn['status'] is False:
            i.frightened = b


#in frightened mod timer stops
def stop_timer():
    game_parameters['stopped timer'] = pygame.time.get_ticks()
    time = time_in_frightened_mod()
    pygame.time.set_timer(HALF_FRIGHTENED_EVENT_ID, 0, True)
    pygame.time.set_timer(FRIGHTENED_EVENT_ID, int(time), True)
    if time > 0:
        if game_parameters['mod'] not in [FRIGHTENED, H_FRIGHTENED]:
            game_parameters['saved mod'] = game_parameters['mod']
        game_parameters['mod'] = FRIGHTENED
        change_frightened(True)


def time_in_frightened_mod():
    return 6000 / 19 * (19 - game_parameters['level'])


# adjusts speed to get to the center of the cell
def correct_move(obj, actions):
        center_x, center_y = cell_center(obj)

        move_x = actions[obj.action][1]
        move_y = actions[obj.action][0]

        next_x = (center_x + move_x) % CELL_SIZE
        next_y = (center_y + move_y) % CELL_SIZE

        if obj.action in VERTICAL:
            if obj.action == RIGHT:
                if center_x < MIDDLE < next_x:
                    move_x = MIDDLE - center_x
            else:
                if center_x > MIDDLE > next_x:
                    move_x = MIDDLE - center_x
        else:
            if obj.action == DOWN:
                if center_y < MIDDLE < next_y:
                    move_y = MIDDLE - center_y
            else:
                if center_y > MIDDLE > next_y:
                    move_y = MIDDLE - center_y
        return (move_x, move_y)


def load_musics():
    MUSIC['munch'] = load_music('munch.wav', key_path='Pac-Man')
    MUSIC['death'] = load_music('death.wav', key_path='Pac-Man')
    MUSIC['eat_ghost'] = load_music('eatghost.wav', key_path='Pac-Man')


def pause_music():
    for key, value in MUSIC.items():
        value.stop()
    pygame.mixer.music.pause()
