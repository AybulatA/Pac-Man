from global_names import *
from tools import *
from Sprites import Target

sprites = load_and_resize_sprites('Blinky')


class Blinky(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.frame = 0
        self.action = LEFT
        self.image = sprites[self.action][self.frame]

        self.target = Target(0, 0, all_sprites)

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        find_action(self)

        sprite_changes(self, sprites)

    def choose_path(self, keys, pos, target):
        if mod == 'scatter':
            self.action = random(keys)
        else:
            if mod == 'frightened':
                target = target_in_frightened_mod['Blinky']

            self.target.rect.x = target[0] * CELL_SIZE
            self.target.rect.y = target[1] * CELL_SIZE

            targeting(self, target, keys, pos)


