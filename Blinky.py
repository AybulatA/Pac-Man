from global_names import *
from tools import *
from Ghost import Ghost


class Blinky(Ghost):
    def __init__(self, pos_x, pos_y, first_gr, second_gr):
        super().__init__(pos_x, pos_y, first_gr, second_gr, 'Blinky')


