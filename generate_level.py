from Sprites import *
from global_names import *
from PacMan import PacMan


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Food(x, y, foods_group, all_sprites)
            elif level[y][x] == '0':
                Energizer(x, y, energizers_group, all_sprites)
    Border(borders_group, all_sprites)
    player = PacMan(30, 10, player_group, all_sprites)
    return player
