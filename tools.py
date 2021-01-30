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


# def load_and_resize_sprites(name):
#     sprites = {
#         'chase': {
#             UP: [],
#             RIGHT: [],
#             DOWN: [],
#             LEFT: []
#         },
#         'dead': []
#     }
#     sprites_pac = {'alive': sprites['chase'].copy(),
#                    'dead': [],
#                    'start_image': [load_image('start.png', colorkey=BLACK, key_path='Pac-Man')]
#                    }
#         self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
#                                 sheet.get_height() // rows)
#         for j in range(rows):
#             for i in range(columns):
#                 frame_location = (self.rect.w * i, self.rect.h * j)
#                 self.frames.append(sheet.subsurface(pygame.Rect(
#                     frame_location, self.rect.size)))
#
#     return resize(sprites)


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


def random(keys):
    return choice(keys)


def possible_keys(obj, actions=actions):
    ans = list()
    coeff = CELL_SIZE // 8

    pos_x = obj.rect.x + CELL_SIZE // 2
    pos_y = obj.rect.y + CELL_SIZE // 2

    acts = {
        RIGHT: (int(pos_x + actions[RIGHT][0] + int(CELL_SIZE * 1.5) - coeff * 7),
                int(pos_y + actions[RIGHT][1])),
        LEFT: (int(pos_x + actions[LEFT][0] - coeff * 3),
               int(pos_y + actions[LEFT][1])),
        DOWN: (int(pos_x + actions[DOWN][0]),
               int(pos_y + actions[DOWN][1] + int(CELL_SIZE * 1.5) - coeff * 7)),
        UP: (int(pos_x + actions[UP][0]),
             int(pos_y + actions[UP][1] - coeff * 3))
    }

    for key, value in acts.items():
        x_cell = (value[0] % LEN_X) // CELL_SIZE
        y_cell = (value[1]) // CELL_SIZE
        if MAP[y_cell][x_cell] in ['.', ' ', '0']:
            if key in [UP, DOWN]:
                x = pos_x % CELL_SIZE
                if x not in [6, 8]:
                    continue
            else:
                y = pos_y % CELL_SIZE
                if y not in [6, 8]:
                    continue
            ans.append(key)
    return ans


def position(obj):
    return [(obj.rect.x + CELL_SIZE // 2) // CELL_SIZE,
            (obj.rect.y + CELL_SIZE // 2) // CELL_SIZE]
