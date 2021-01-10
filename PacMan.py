from global_names import *
from tools import *
import pygame


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
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
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

        self.score = 0

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
        if len(pygame.sprite.spritecollide(self, foods_group, True)) == 1:
            self.score += 10
        if len(pygame.sprite.spritecollide(self, energizers_group, True)) == 1:
            self.score += 50
        print(self.score)


