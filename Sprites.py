from tools import load_image
from global_names import *


class Border(pygame.sprite.Sprite):
    def __init__(self, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.transform.scale(load_image('field.jpg', colorkey=BLACK),
                                            (CELL_SIZE * 28, CELL_SIZE * 31))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.Surface([4, 4])
        pygame.draw.rect(self.image, FOODS_COLOR, (0, 0, 4, 4))
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x + CELL_SIZE // 2 - 2, CELL_SIZE * pos_y + CELL_SIZE // 2 - 2)


class Energizer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)

        first = pygame.Surface([CELL_SIZE, CELL_SIZE])
        pygame.draw.circle(first, FOODS_COLOR, (CELL_SIZE // 2,
                           CELL_SIZE // 2), CELL_SIZE // 2)

        second = pygame.Surface([CELL_SIZE, CELL_SIZE])

        self.frame = 0
        self.sprites = [first, second]
        self.image = self.sprites[self.frame]
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, CELL_SIZE * pos_y)

    def update(self):
        self.frame = (self.frame + 0.1) % len(self.sprites)
        self.image = self.sprites[int(self.frame)]


#class Score(pygame.sprite.Sprite):
#    def __init__(self, gr):
#        super().__init__(gr)


class Target(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr):
        super().__init__(first_gr)
        self.image = pygame.transform.scale(load_image('cross.jpg'), (int(CELL_SIZE),
                                                        int(CELL_SIZE)))
        self.rect = self.image.get_rect().move(
            CELL_SIZE * pos_x, CELL_SIZE * pos_y)
