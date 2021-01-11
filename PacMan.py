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

#changing size of image
for i in pacman_sprites.keys():
    for j in range(len(pacman_sprites[i])):
        el = pacman_sprites[i][j]
        pacman_sprites[i][j] = pygame.transform.scale(el, (CELL_SIZE + CELL_SIZE // 2,
                                                           CELL_SIZE + CELL_SIZE // 2))

pacman_sprites[DOWN] = [pygame.transform.flip(pacman_sprites[UP][0], False, True),
                        pygame.transform.flip(pacman_sprites[UP][1], False, True)]

pacman_sprites[LEFT] = [pygame.transform.flip(pacman_sprites[RIGHT][0], True, False),
                        pygame.transform.flip(pacman_sprites[RIGHT][1], True, False)]


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr, border, map):
        super().__init__(first_gr, second_gr)
        self.image = pacman_sprites['start_image'][0]
        self.frame = 0
        self.action = None

        #for check collision of masks
        self.border = border

        #for check position of Pac-Man
        self.map = map

        self.rect = self.image.get_rect().move(CELL_SIZE * (pos_x + 1) + CELL_SIZE // 4,
                                               CELL_SIZE * (pos_y + 1) - CELL_SIZE // 4)
        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0

    def key_pressed(self, key):
        if key in self.possible_keys():
            self.action = key

    def possible_keys(self):
        #find center of the Pac-Man, bcs sprite is bigger then one cell
        pos_x = (self.rect.x + self.rect.w // 2) // CELL_SIZE
        pos_y = (self.rect.y + self.rect.h // 2) // CELL_SIZE

        ans = list()

        free_cells = ['.', ' ', '0']

        if self.map[pos_y + 1][pos_x] in free_cells:
            ans.append(DOWN)
        if self.map[pos_y - 1][pos_x] in free_cells:
            ans.append(UP)
        if pos_x < 27:
            if self.map[pos_y][pos_x - 1] in free_cells:
                ans.append(LEFT)
            if self.map[pos_y][pos_x + 1] in free_cells:
                ans.append(RIGHT)
        return ans

    def update(self):
        if self.action is not None and not pygame.sprite.collide_mask(self, self.border)\
                or self.action in self.possible_keys():
            self.frame = (self.frame + 0.4) % 2
            self.image = pacman_sprites[self.action][int(self.frame)]
            self.mask = pygame.mask.from_surface(self.image)

            self.rect.x = (self.rect.x + actions[self.action][1]) % (CELL_SIZE * 26)
            self.rect.y = (self.rect.y + actions[self.action][0]) % (CELL_SIZE * 29)
        if len(pygame.sprite.spritecollide(self, foods_group, True)) == 1:
            self.score += 10
        if len(pygame.sprite.spritecollide(self, energizers_group, True)) == 1:
            self.score += 50


