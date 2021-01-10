from tools import load_image
from global_names import *


tile_images = {
    #'house': load_image('house_type21_NW.png'),
    #'road': load_image('driveway_long_SE.png'),
    #'player': load_image('be819cfceb34c029ee5764071deb1efb.png')
}


up = [load_image('pac-man_up(first).png', colorkey=BLACK),
      load_image('pac-man_up(second).png', colorkey=BLACK)]
right = [load_image('pac-man_right(first).png', colorkey=BLACK),
         load_image('pac-man_right(second).png', colorkey=BLACK)]
for i in range(len(up)):
    up[i] = pygame.transform.scale(up[i], (CELL_SIZE_X, CELL_SIZE_Y))
for i in range(len(right)):
    right[i] = pygame.transform.scale(right[i], (CELL_SIZE_X, CELL_SIZE_Y))


pacman_sprites = {
    UP: up,
    DOWN: [pygame.transform.flip(up[0], False, True),
           pygame.transform.flip(up[1], False, True)],
    RIGHT: right,
    LEFT: [pygame.transform.flip(right[0], True, False),
           pygame.transform.flip(right[1], True, False)],
}


class PacMan(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = load_image('pac-man(start).png', colorkey=BLACK)
        self.frame = 0
        self.action = {
            'key': None,
            'action': None
        }
        self.rect = self.image.get_rect().move(
            CELL_SIZE * (pos_x + 1), CELL_SIZE * pos_y + CELL_SIZE // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def key_pressed(self, key):
        if key in actions.keys():
            self.action['action'] = actions[key]
            self.action['key'] = key

    def update(self):
        if self.action['key'] is not None and not pygame.sprite.spritecollideany(self, borders_group):
            self.frame = (self.frame + 0.4) % 2
            self.image = pacman_sprites[self.action['key']][int(self.frame)]
            self.rect.x += self.action['action'][1]
            self.rect.y += self.action['action'][0]


class Border(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.Surface([CELL_SIZE_X, CELL_SIZE_Y])
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, CELL_SIZE_X, CELL_SIZE_Y))
        self.rect = self.image.get_rect().move(
            CELL_SIZE_X * pos_x, CELL_SIZE_Y * pos_y)


class Food(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            400 * pos_x, 400 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Energizer(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            400 * pos_x, 400 * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

