from Sprites import *
from global_names import *


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '*':
                continue
                Border(x, y, borders_group, all_sprites)
            elif level[y][x] == '.':
                pass
                #Food('road', x, y, foods_group, all_sprites)
            elif level[y][x] == '0':
                pass
                #Energizer('road', x, y, foods_group, all_sprites)
    player = PacMan('player', 30, 10, player_group, all_sprites)
    return player
