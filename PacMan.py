from global_names import *
from tools import *
import pygame

sprites = load_and_resize_sprites('Pac-Man')


class PacMan(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.frame = 0
        self.action = LEFT
        self.image = sprites['start_image'][self.frame]
        self.temporary_action = None

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

        self.mask = pygame.mask.from_surface(self.image)
        self.score = 0

    def key_pressed(self, key):
        if key in possible_keys(self):
            self.action = key
        else:
            self.temporary_action = ((self.rect.x, self.rect.y), key)

    def update(self):
        if self.action in possible_keys(self):
            path = sprites['alive'][self.action]
            self.frame = (self.frame + 0.2) % len(path)
            self.image = path[int(self.frame)]
            self.mask = pygame.mask.from_surface(self.image)

            self.rect.x = (self.rect.x + actions[self.action][1]) % LEN_X
            self.rect.y = (self.rect.y + actions[self.action][0])

        #helps to turn at corners
        if self.temporary_action is not None:
            cells_passed = abs(self.rect.x - self.temporary_action[0][0]) // CELL_SIZE\
                           + abs(self.rect.y - self.temporary_action[0][1]) // CELL_SIZE
            if cells_passed <= 1:
                if self.temporary_action[1] in possible_keys(self):
                    self.action = self.temporary_action[1]
                    self.temporary_action = None
            else:
                self.temporary_action = None

        if len(pygame.sprite.spritecollide(self, foods_group, True)) == 1:
            self.score += 10
        if len(pygame.sprite.spritecollide(self, energizers_group, True)) == 1:
            self.score += 50
            game_parameters['mod'] = 'frightened'


