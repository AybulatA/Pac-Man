from tools import load_image
from global_names import *


tile_images = {
    #'house': load_image('house_type21_NW.png'),
    #'road': load_image('driveway_long_SE.png'),
    #'player': load_image('be819cfceb34c029ee5764071deb1efb.png')
}


class Border(pygame.sprite.Sprite):
    def __init__(self, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.transform.scale(load_image('field.jpg', colorkey=BLACK).convert_alpha(), (CELL_SIZE * 28, CELL_SIZE * 31))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class Food(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.Surface([4, 4])
        pygame.draw.rect(self.image, FOODS_COLOR, (0, 0, 4, 4))
        self.rect = self.image.get_rect().move(
            CELL_SIZE_X * pos_x + CELL_SIZE_X // 2, CELL_SIZE_Y * pos_y + CELL_SIZE_Y // 2)


class Energizer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(first_gr, second_gr)
        self.image = pygame.Surface([CELL_SIZE_X, CELL_SIZE_Y])
        pygame.draw.circle(self.image, FOODS_COLOR, (CELL_SIZE_X // 2,
                           CELL_SIZE_Y // 2), CELL_SIZE // 2)
        self.rect = self.image.get_rect().move(
            CELL_SIZE_X * pos_x, CELL_SIZE_Y * pos_y)

