from global_names import *
from tools import *

sprites = load_and_resize_sprites('Pinky')


class Pinky(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr, player):
        super().__init__(first_gr, second_gr)
        self.frame = 0
        self.action = LEFT
        self.image = sprites[self.action][self.frame]

        self.player = player

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        keys = possible_keys(self)

        #ghosts can't turn around
        if opposite_keys[self.action] in keys:
            keys.remove(opposite_keys[self.action])

        pos = ((self.rect.x + CELL_SIZE // 2) // CELL_SIZE,
               (self.rect.y + CELL_SIZE // 2) // CELL_SIZE)

        if len(keys) > 1:
            self.choose_path(keys, pos)
        else:
            self.action = keys[0]

        sprite_changes(self, sprites)

    def choose_path(self, keys, pos):
        target = [(self.player.rect.x + CELL_SIZE // 2) // CELL_SIZE,
                  (self.player.rect.y + CELL_SIZE // 2) // CELL_SIZE]

        act = self.player.action
        if act in VERTICAL:
            target[0] = (-1) ** VERTICAL.index(act) * 4 + target[0]
            target[1] = target[1]
        else:
            target[0] = target[0]
            target[1] = (-1) ** HORIZONTAL.index(act) * 4 + target[1]

        targeting(self, target, keys, pos)

