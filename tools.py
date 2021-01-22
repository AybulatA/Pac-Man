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
