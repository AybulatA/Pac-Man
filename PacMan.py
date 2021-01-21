from global_names import *
from tools import *
import pygame


pacman_sprites = {
    UP: [load_image('pac-man_up(first).png', colorkey=BLACK),
         load_image('pac-man_up(second).png', colorkey=BLACK)],
    RIGHT: [load_image('pac-man_right(first).png', colorkey=BLACK),
            load_image('pac-man_right(second).png', colorkey=BLACK)],
    'start_image': [load_image('pac-man(start).png', colorkey=BLACK)]
}

#changing size of images
for i in pacman_sprites.keys():
    for j in range(len(pacman_sprites[i])):
        el = pacman_sprites[i][j]
        pacman_sprites[i][j] = pygame.transform.scale(el, (int(CELL_SIZE * 1.5),
                                                           int(CELL_SIZE * 1.5)))

pacman_sprites[DOWN] = [pygame.transform.flip(pacman_sprites[UP][0], False, True),
                        pygame.transform.flip(pacman_sprites[UP][1], False, True)]

pacman_sprites[LEFT] = [pygame.transform.flip(pacman_sprites[RIGHT][0], True, False),
                        pygame.transform.flip(pacman_sprites[RIGHT][1], True, False)]


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr, border, map):
        super().__init__(first_gr, second_gr)
        self.image = pacman_sprites['start_image'][0]
        self.frame = 0
        self.action = LEFT
        self.temporary_action = None

        #for check collision of masks
        self.border = border

        self.rect = self.image.get_rect().move(CELL_SIZE * (pos_x + 1) - CELL_SIZE // 4,
                                               CELL_SIZE * (pos_y + 1) - CELL_SIZE // 4)

        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0

    def key_pressed(self, key):
        if key in possible_keys(self):
            self.action = key
        else:
            self.temporary_action = ((self.rect.x, self.rect.y), key)

    def update(self):
        col = pygame.sprite.collide_mask(self, self.border)
        if col is not None:
            print(col)
        if self.action in possible_keys(self):
            self.frame = (self.frame + 0.3) % 2
            self.image = pacman_sprites[self.action][int(self.frame)]
            self.mask = pygame.mask.from_surface(self.image)

            self.rect.x = (self.rect.x + actions[self.action][1]) % LEN_X
            self.rect.y = (self.rect.y + actions[self.action][0])

        #helps to turn at corners
        if self.temporary_action is not None:
            cells_passed = abs(self.rect.x - self.temporary_action[0][0]) // CELL_SIZE\
                           + abs(self.rect.y - self.temporary_action[0][1]) // CELL_SIZE
            if cells_passed <= 2:
                if self.temporary_action[1] in possible_keys(self):
                    self.action = self.temporary_action[1]
                    self.temporary_action = None
            else:
                self.temporary_action = None

        if len(pygame.sprite.spritecollide(self, foods_group, True)) == 1:
            self.score += 10
        if len(pygame.sprite.spritecollide(self, energizers_group, True)) == 1:
            self.score += 50


