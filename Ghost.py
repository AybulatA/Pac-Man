from global_names import *
from tools import *
from Sprites import Target


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr, name):
        super().__init__(first_gr, second_gr)

        self.frame = 0
        self.action = LEFT

        self.name = name
        self.sprites = load_and_resize_sprites(self.name)
        self.image = self.sprites[game_parameters['mod']][self.action][self.frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.target = Target(0, 0, all_sprites)

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

    def update(self):
        keys = find_action(self)

        if game_parameters['mod'] == 'frightened':
            self.action = random(keys)
        elif len(keys) < 1:
            self.action = keys[0]
        else:
            if game_parameters['mod'] == 'scatter':
                target = target_in_scatter_mod[self.name]
            else:
                target = self.choose_path()

            targeting(self, target, keys)

        sprite_changes(self, self.sprites)

    def choose_path(self):

        target = [(characters_obj['Pac-Man'].rect.x + CELL_SIZE // 2) // CELL_SIZE,
                  (characters_obj['Pac-Man'].rect.y + CELL_SIZE // 2) // CELL_SIZE]

        target = self.new_target(target)

        self.target.rect.x = target[0] * CELL_SIZE
        self.target.rect.y = target[1] * CELL_SIZE

        return target


    def new_target(self, target):
        return target
