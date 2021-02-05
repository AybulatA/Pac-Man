from global_names import *
from tools import *
from Sprites import Target


class Ghost(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr, name):
        super().__init__(first_gr, second_gr)

        self.frame = 0
        self.action = UP

        self.name = name
        self.sprites = load_and_resize_sprites(self.name)
        self.image = self.sprites[game_parameters['mod']][self.frame]
        self.mask = pygame.mask.from_surface(self.image)

<<<<<<< HEAD
        self.last_cell_action = [0, 0]
=======
        self.last_action_pos = [-1, -1]
>>>>>>> 0d058d1405e25df7874f057f355b4da4e68d3f7b

        self.target = Target(0, 0, all_sprites)

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

        self.real_rect_x = self.rect.x
        self.real_rect_y = self.rect.y

    def update(self):
        keys = self.find_action()
        if len(keys) == 1:
            self.action = keys[0]
        else:
            if position(self) in ACTION_CELLS and self.last_cell_action != position(self):
                if game_parameters['mod'] == 'frightened':
                    self.action = random(keys)
                else:
                    if game_parameters['mod'] == 'scatter':
                        target = target_in_scatter_mod[self.name]
                    else:
                        target = self.choose_path()

                    self.targeting(target, keys)

                self.last_cell_action = position(self)

        self.sprite_changes()

    def sprite_changes(self):
        if game_parameters['mod'] == 'chase':
            path = self.sprites[game_parameters['mod']][self.action]
        else:
            path = self.sprites[game_parameters['mod']]

        actions = self.ghost_speed_change()
        self.frame = (self.frame + 0.2) % len(path)
        self.image = path[int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

        self.real_rect_x = (self.real_rect_x + actions[self.action][1]) % LEN_X
        self.real_rect_y = (self.real_rect_y + actions[self.action][0])

        self.rect.x = int(self.real_rect_x)
        self.rect.y = int(self.real_rect_y)

    def ghost_speed_change(self):
        if game_parameters['mod'] == 'frightened':
            speed = MODS_SPEED['frightened']
        elif position(self) in TUNNEL_CELLS:
            speed = MODS_SPEED['tunnel']
        elif game_parameters['mod'] == 'chase' or game_parameters['mod'] == 'scatter':
            speed = self.default_speed()
        else:
            speed = 3
        return {
            RIGHT: (0, speed),
            LEFT: (0, -speed),
            DOWN: (speed, 0),
            UP: (-speed, 0),
        }

    def default_speed(self):
        return MODS_SPEED['chase']

    def choose_path(self):
        target = [(characters_obj['Pac-Man'].rect.x + CELL_SIZE // 2) // CELL_SIZE,
                  (characters_obj['Pac-Man'].rect.y + CELL_SIZE // 2) // CELL_SIZE]

        target = self.new_target(target)

        self.target.rect.x = target[0] * CELL_SIZE
        self.target.rect.y = target[1] * CELL_SIZE

        return target

    def new_target(self, target):
        return target

    def find_action(self):
        keys = possible_keys(self, self.ghost_speed_change())

        if len(keys) == 1:
            return keys

        #ghosts can't turn around
        if opposite_keys[self.action] in keys:
            keys.remove(opposite_keys[self.action])

        pos = position(self)
        #ghosts on these cells cannot turn up
        if pos in BLOCK_CELLS:
            if UP in keys:
                keys.remove(UP)

        return keys

    def targeting(self, target, keys):
        pos = position(self)

        ans = list()

        for i in keys:
            if i in VERTICAL:
                x = (-1) ** VERTICAL.index(i) + pos[0]
                y = pos[1]
            else:
                x = pos[0]
                y = (-1) ** HORIZONTAL.index(i) + pos[1]
            line = (abs(target[0] - x) ** 2 + abs(target[1] - y) ** 2) ** 0.5
            ans.append((i, (x, y), line))

        ans = sorted(ans, key=lambda z: z[-1])

        if ans[0][-1] == ans[-1][-1] and len(ans) != 1:
            #if all ways have the same length, the way will be chosen by priority
            priority = [UP, LEFT, DOWN]
            ans = sorted(ans, key=lambda z: priority.index(z[0]) if z[0] in priority else 10)

        self.action = ans[0][0]
<<<<<<< HEAD
=======
        self.last_action_pos = [self.rect.x, self.rect.y]
>>>>>>> 0d058d1405e25df7874f057f355b4da4e68d3f7b


