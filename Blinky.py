from global_names import *
from tools import *

sprites = load_and_resize_sprites('Blinky')


class Blinky(pygame.sprite.Sprite):
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

        self.frame = (self.frame + 0.3) % 2
        self.image = sprites[self.action][int(self.frame)]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.x = (self.rect.x + actions[self.action][1]) % LEN_X
        self.rect.y = (self.rect.y + actions[self.action][0])

    def choose_path(self, keys, pos):
        ans = list()
        target = ((self.player.rect.x + CELL_SIZE // 2) // CELL_SIZE,
                  (self.player.rect.y + CELL_SIZE // 2) // CELL_SIZE)

        #hosts on these cells cannot turn up
        if pos in [(12, 11), (15, 11), (15, 23), (12, 23)]:
            if UP in keys:
                keys.remove(UP)
                self.action = keys[0]
                pass

        vertical = [RIGHT, LEFT]
        horizontal = [DOWN, UP]

        for i in keys:
            if i in vertical:
                x = (-1) ** vertical.index(i) + pos[0]
                y = pos[1]
            else:
                x = pos[0]
                y = (-1) ** horizontal.index(i) + pos[1]
            line = (abs(target[0] - x) ** 2 + abs(target[1] - y)) ** 0.5
            ans.append((i, (x, y), line))

        sorted_ans = sorted(ans, key=lambda z: z[-1])
        if sorted_ans[0][-1] == sorted_ans[-1][-1]:

            #if all ways the same, the way will be chosen by priority
            priority = [UP, LEFT, DOWN]
            sorted_ans = sorted(ans, key=lambda z: priority.index(z[0]) if z[0] in priority else 0)
        self.action = sorted_ans[0][0]

