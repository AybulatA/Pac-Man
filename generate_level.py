from Sprites import *
from global_names import *
from PacMan import PacMan
from Blinky import Blinky
from Pinky import Pinky
from Inky import Inky
from Clyde import Clyde


def generate_level(level):
    Border(borders_group, all_sprites)

    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Food(x, y, foods_group, all_sprites)
            elif level[y][x] == '0':
                Energizer(x, y, energizers_group, all_sprites)

    game_obj['Pac-Man'] = PacMan(15, 8, player_group, all_sprites)
    game_obj['Blinky'] = Blinky(10, 1, enemy_group, all_sprites)
#    game_obj['score'] = Score(all_sprites)
    Pinky(6, 22, enemy_group, all_sprites)
    Inky(15, 5, enemy_group, all_sprites)
    Clyde(1, 22, enemy_group, all_sprites)


