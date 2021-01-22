import os
import sys
from global_names import *


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


def load_and_resize_sprites(name):
    sprites = {
        UP: [load_image('up(first).png', colorkey=BLACK, key_path=name),
             load_image('up(second).png', colorkey=BLACK, key_path=name)],
        RIGHT: [load_image('right(first).png', colorkey=BLACK, key_path=name),
                load_image('right(second).png', colorkey=BLACK, key_path=name)]
    }
    if name == 'Pac-Man':
        sprites[DOWN] = [pygame.transform.flip(sprites[UP][0], False, True),
                         pygame.transform.flip(sprites[UP][1], False, True)]

        sprites[LEFT] = [pygame.transform.flip(sprites[RIGHT][0], True, False),
                         pygame.transform.flip(sprites[RIGHT][1], True, False)]

        sprites['start_image'] = [load_image('start.png',
                                             colorkey=BLACK, key_path=name)]
    else:
        sprites[DOWN] = [load_image('down(first).png', colorkey=BLACK, key_path=name),
                         load_image('down(second).png', colorkey=BLACK, key_path=name)]

        sprites[LEFT] = [load_image('left(first).png', colorkey=BLACK, key_path=name),
                         load_image('left(second).png', colorkey=BLACK, key_path=name)]

    #changing size of images
    for i in sprites.keys():
        for j in range(len(sprites[i])):
            el = sprites[i][j]
            sprites[i][j] = pygame.transform.scale(el, (int(CELL_SIZE * 1.5),
                                                        int(CELL_SIZE * 1.5)))
    return sprites


def targeting(obj, target, keys, pos):
    #ghosts on these cells cannot turn up
    if pos in [(12, 11), (15, 11), (15, 23), (12, 23)]:
        if UP in keys:
            keys.remove(UP)
            obj.action = keys[0]

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

        #if all ways the same, the way will be chosen by priority
        priority = [UP, LEFT, DOWN]
        ans = sorted(ans, key=lambda z: priority.index(z[0]) if z[0] in priority else 10)
        print(ans)

    obj.action = ans[0][0]


def sprite_changes(obj, sprites):
    obj.frame = (obj.frame + 0.3) % 2
    obj.image = sprites[obj.action][int(obj.frame)]
    obj.mask = pygame.mask.from_surface(obj.image)

    obj.rect.x = (obj.rect.x + actions[obj.action][1]) % LEN_X
    obj.rect.y = (obj.rect.y + actions[obj.action][0])
