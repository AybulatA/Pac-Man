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
        self.alive = True

        self.rect = self.image.get_rect().move(CELL_SIZE * pos_x - CELL_SIZE // 4,
                                               CELL_SIZE * pos_y - CELL_SIZE // 4)

        self.mask = pygame.mask.from_surface(self.image)

        self.real_rect_x = self.rect.x
        self.real_rect_y = self.rect.y

    def key_pressed(self, key):
        if key in possible_keys(self):
            self.action = key
        else:
            self.temporary_action = ((self.rect.x, self.rect.y), key)

    def dead(self):
        self.alive = False
        for i in enemy_group:
            i.kill()
        self.action = None

    def update(self):
        score = 0
        mod = game_parameters['mod']
        enemy = pygame.sprite.spritecollide(self, enemy_group, False)
        if len(enemy) != 0:
            enemy = enemy[0]
            if position(self) == position(enemy) and enemy.alive is True:
                if mod == FRIGHTENED or mod == H_FRIGHTENED:
                    game_parameters['ate ghosts'] += 1
                    game_parameters['mod'] = STOP
                    enemy.dead()
                    score += (2 ** game_parameters['ate ghosts']) * 200
                else:
                    self.dead()
                    self.frame = 0

        if self.alive is False:
            frame_speed = 0.075
        else:
            frame_speed = 0.2

        if self.action in possible_keys(self) or self.alive is False:
            if self.alive is True:
                path = sprites['alive'][self.action]
            else:
                path = sprites['dead']
            self.frame = self.frame + frame_speed

            if self.frame >= len(sprites['dead']) and self.alive is False:
                kill_attempt_and_reset_game()
                return None

            if self.alive:
                self.frame = self.frame % len(path)

            self.image = path[int(self.frame)]
            self.mask = pygame.mask.from_surface(self.image)

            if self.alive is True:
                self.real_rect_x = (self.real_rect_x + actions[self.action][1]) % LEN_X
                self.real_rect_y = (self.real_rect_y + actions[self.action][0])

                self.rect.x = int(self.real_rect_x)
                self.rect.y = int(self.real_rect_y)

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
            score += 10
        if len(pygame.sprite.spritecollide(self, energizers_group, True)) == 1:
            game_parameters['saved mod'] = game_parameters['mod']
            game_parameters['mod'] = FRIGHTENED
            change_frightened(True)
            score += 50
            stop_timer()
            change_way()
        game_parameters['score'] += score
