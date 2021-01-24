import os
import sys
from global_names import *
from random import choice


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
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    global MAP
    filename = "data/" + filename
    with open(filename, encoding='utf-8') as mapFile:
        MAP = [line for line in mapFile]
    return MAP


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


def possible_keys(obj):
    ans = list()
    coeff = CELL_SIZE // 8

    pos_x = obj.rect.x + CELL_SIZE // 2
    pos_y = obj.rect.y + CELL_SIZE // 2

    acts = {
        RIGHT: (pos_x + actions[RIGHT][0] + int(CELL_SIZE * 1.5) - coeff * 7,
                pos_y + actions[RIGHT][1]),
        LEFT: (pos_x + actions[LEFT][0] - coeff * 3,
               pos_y + actions[LEFT][1]),
        DOWN: (pos_x + actions[DOWN][0],
               pos_y + actions[DOWN][1] + int(CELL_SIZE * 1.5) - coeff * 7),
        UP: (pos_x + actions[UP][0],
             pos_y + actions[UP][1] - coeff * 3)
    }

    for key, value in acts.items():
        x_cell = (value[0] % LEN_X) // CELL_SIZE
        y_cell = (value[1]) // CELL_SIZE
        if MAP[y_cell][x_cell] in ['.', ' ', '0']:
            if key in [UP, DOWN]:
                if pos_x % CELL_SIZE not in [6, 8]:
                    continue
            else:
                if pos_y % CELL_SIZE not in [6, 8]:
                    continue
            ans.append(key)
    return ans


def load_pacman_sprites(sprites):
    sprites_pac = {'alive': sprites['chase'].copy(),
                   'dead': [],
                   'start_image': [load_image('start.png', colorkey=BLACK, key_path='Pac-Man')]
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
        sprites_pac['dead'].append(load_image(n, colorkey=BLACK, key_path='Pac-Man'))

    return sprites_pac


def load_and_resize_sprites(name):
    sprites = {
        'chase': {
            UP: [load_image('up(first).png', colorkey=BLACK, key_path=name),
                 load_image('up(second).png', colorkey=BLACK, key_path=name)],
            RIGHT: [load_image('right(first).png', colorkey=BLACK, key_path=name),
                    load_image('right(second).png', colorkey=BLACK, key_path=name)],
            DOWN: [],
            LEFT: []
        },
        'dead': []
    }
    if name == 'Pac-Man':
        sprites = load_pacman_sprites(sprites)
    else:
        f = [load_image('frightened(first).png', colorkey=BLACK, key_path='Ghost'),
             load_image('frightened(second).png', colorkey=BLACK, key_path='Ghost')]
        sprites['frightened'] = f.copy()

        f.append(load_image('half_frightened(first).png', colorkey=BLACK, key_path='Ghost'))
        f.append(load_image('half_frightened(second).png', colorkey=BLACK, key_path='Ghost'))

        sprites['half_frightened'] = f.copy()

        sprites['chase'][DOWN] = [load_image('down(first).png', colorkey=BLACK, key_path=name),
                                  load_image('down(second).png', colorkey=BLACK, key_path=name)]

        sprites['chase'][LEFT] = [load_image('left(first).png', colorkey=BLACK, key_path=name),
                                  load_image('left(second).png', colorkey=BLACK, key_path=name)]

    return resize(sprites)


def resize(sprites):
    for z in sprites:
        if z == 'chase' or z == 'alive':
            for i in sprites[z]:
                for j in range(len(sprites[z][i])):
                    el = sprites[z][i][j]
                    sprites[z][i][j] = pygame.transform.scale(el, (int(CELL_SIZE * 1.5),
                                                                   int(CELL_SIZE * 1.5)))
        else:
            for i in range(len(sprites[z])):
                el = sprites[z][i]
                sprites[z][i] = pygame.transform.scale(el, (int(CELL_SIZE * 1.5),
                                                            int(CELL_SIZE * 1.5)))

    return sprites


def targeting(obj, target, keys):
    pos = position(obj)

    ans = list()

    for i in keys:
        if i in VERTICAL:
            x = (-1) ** VERTICAL.index(i) + pos[0]
            y = pos[1]
        else:
            x = pos[0]
            y = (-1) ** HORIZONTAL.index(i) + pos[1]
        line = (abs(target[0] - x) ** 2 + abs(target[1] - y) ** 2) ** 0.5
        ans.append((i, (x, y), line))

    ans = sorted(ans, key=lambda z: z[-1])

    if ans[0][-1] == ans[-1][-1] and len(ans) != 1:

        #if all ways have the same length, the way will be chosen by priority
        priority = [UP, LEFT, DOWN]
        ans = sorted(ans, key=lambda z: priority.index(z[0]) if z[0] in priority else 10)

    obj.action = ans[0][0]


def sprite_changes(obj, sprites):
    if game_parameters['mod'] == 'chase':
        path = sprites[game_parameters['mod']][obj.action]
    else:
        path = sprites[game_parameters['mod']]
    obj.frame = (obj.frame + 0.2) % len(path)
    obj.image = path[int(obj.frame)]
    obj.mask = pygame.mask.from_surface(obj.image)

    obj.rect.x = (obj.rect.x + actions[obj.action][1]) % LEN_X
    obj.rect.y = (obj.rect.y + actions[obj.action][0])


def find_action(obj):
    keys = possible_keys(obj)

    #ghosts can't turn around
    if opposite_keys[obj.action] in keys:
        keys.remove(opposite_keys[obj.action])

    pos = position(obj)
    #ghosts on these cells cannot turn up
    if pos in [[12, 11], [15, 11], [15, 23], [12, 23]]:
        if UP in keys:
            keys.remove(UP)
            obj.action = keys[0]

    return keys


def random(keys):
    return choice(keys)


def position(obj):
    return [(obj.rect.x + CELL_SIZE // 2) // CELL_SIZE,
            (obj.rect.y + CELL_SIZE // 2) // CELL_SIZE]
