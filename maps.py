# Creator: rafaelurben

import pygame
from random import randint

from coordinates import sin, coord_distance

class Map:
    def __init__(self, width, height, spawnpoint, mymap=[], spawn_range=5):
        self.width = width
        self.height = height
        self.map = mymap

        self.spawnpoint = spawnpoint
        self.spawn_range = spawn_range

        self.blocks_horizontal = len(self.map[0])
        self.blocks_vertical = len(self.map)
        self.block_width = self.width/self.blocks_horizontal
        self.block_height = self.height/self.blocks_vertical

    def random_spawn(self):
        return (randint(self.spawnpoint[0]-self.spawn_range, self.spawnpoint[0]+self.spawn_range), randint(self.spawnpoint[1]-self.spawn_range, self.spawnpoint[1]+self.spawn_range))

    def draw(self, win):
        for r, row in enumerate(self.map):
            for c, color in enumerate(row):
                rect = ((c*self.block_width,r*self.block_height),((c+1)*self.block_width,(r+1)*self.block_height))
                pygame.draw.rect(win, color, rect)

# Utility functions

    def get_block_at(self, x, y):
        '''Get the block at specified coordinates'''

        return self.map[int(y/self.block_height)][int(x/self.block_width)]

    def touches_black(self, x, y, radius):
        '''Check if there's black in a given pixel range'''

        # d = sin(45)*radius

        blocks = [
            (x,         y),
            (x-radius,  y),
            (x+radius,  y),
            (x,         y-radius),
            (x,         y+radius),
            # (x+d,       y+d),
            # (x+d,       y-d),
            # (x-d,       y+d),
            # (x-d,       y-d),
        ]

        for block in blocks:
            if self.get_block_at(*block) == (0,0,0):
                return True

        # Bei Diagonalen Entfernung zu Ecken berechnen

        return False

# Colors

b       = (  0,   0,   0)
w       = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)

# Maps

DEFAULT_MAP = Map(width=800, height=400, spawnpoint=(115, 230) , mymap=[
    (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,),
    (b,b,w,w,w,w,w,w,w,w,w,w,b,b,b,b,),
    (b,w,w,w,b,w,w,b,b,w,w,w,w,b,b,b,),
    (b,w,w,w,b,w,w,w,b,b,w,b,w,w,b,b,),
    (b,w,w,w,b,w,b,w,w,w,w,b,b,w,w,b,),
    (b,w,w,w,w,w,w,w,w,w,w,b,b,w,w,b,),
    (b,b,w,w,b,w,b,w,w,w,w,w,w,w,b,b,),
    (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,),
])