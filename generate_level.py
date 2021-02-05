from Sprites import *
from global_names import *
from PacMan import PacMan
from Blinky import Blinky
from Pinky import Pinky
from Inky import Inky
from Clyde import Clyde


def generate_level(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Food(x, y, foods_group, all_sprites)
            elif level[y][x] == '0':
                Energizer(x, y, energizers_group, all_sprites)
    Border(borders_group, all_sprites)
<<<<<<< HEAD
    characters_obj['Pac-Man'] = PacMan(5, 5, player_group, all_sprites)
    characters_obj['Blinky'] = Blinky(6, 10, enemy_groups, all_sprites)
    for i in ACTION_CELLS:
        Target(i[0], i[1], all_sprites)
=======
    characters_obj['Pac-Man'] = PacMan(1, 1, player_group, all_sprites)
    #characters_obj['Blinky'] = Blinky(2, 14, enemy_groups, all_sprites)
>>>>>>> 0d058d1405e25df7874f057f355b4da4e68d3f7b
    #Pinky(2, 22, enemy_groups, all_sprites)
    #Inky(15, 2, enemy_groups, all_sprites)
    #Clyde(1, 22, enemy_groups, all_sprites)
