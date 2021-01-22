from Sprites import *
from global_names import *
from PacMan import PacMan
from Blinky import Blinky
from Pinky import Pinky


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Food(x, y, foods_group, all_sprites)
            elif level[y][x] == '0':
                Energizer(x, y, energizers_group, all_sprites)
    border = Border(borders_group, all_sprites)
    player = PacMan(12, 22, player_group, all_sprites)
    Blinky(12, 8, enemy_groups, all_sprites, player)
    Pinky(2, 2, enemy_groups, all_sprites, player)
    return player, border
