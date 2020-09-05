# Creator: https://github.com/rafaelurben

# Imports

import pygame
from random import randint

# Relative Imports

from .coordinates import ceil, floor, sin, coord_distance

# Classes

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

        self.UNTOUCHABLE_COLORS = [(0, 0, 0)]

    def random_spawn(self):
        return (randint(self.spawnpoint[0]-self.spawn_range, self.spawnpoint[0]+self.spawn_range), randint(self.spawnpoint[1]-self.spawn_range, self.spawnpoint[1]+self.spawn_range))

    def draw(self, win):
        for r, row in enumerate(self.map):
            for c, color in enumerate(row):
                rect = ((c*self.block_width,r*self.block_height),((c+1)*self.block_width,(r+1)*self.block_height))
                pygame.draw.rect(win, color, rect)

# Utility functions

    def get_block_at(self, x, y):
        '''Get the block color at specified coordinates'''

        return self.map[int(y/self.block_height)][int(x/self.block_width)]

    def get_corner_blocks(self, x, y):
        '''Get the color and the nearest coordinate of corners blocks.'''

        corners = [
            (
                (floor(x/self.block_width)*self.block_width, floor(y/self.block_height)*self.block_height), 
                self.get_block_at(abs(x-self.block_width), abs(y-self.block_height))
            ),
            (
                (ceil(x/self.block_width)*self.block_width,  floor(y/self.block_height)*self.block_height), 
                self.get_block_at(abs(x+self.block_width), abs(y-self.block_height))
            ),
            (
                (floor(x/self.block_width)*self.block_width, ceil(y/self.block_height)*self.block_height),  
                self.get_block_at(abs(x-self.block_width), abs(y+self.block_height))
            ),
            (
                (ceil(x/self.block_width)*self.block_width,  ceil(y/self.block_height)*self.block_height),  
                self.get_block_at(abs(x+self.block_width), abs(y+self.block_height))
            ),
        ]
        return corners


    def touches_black(self, x, y, radius):
        '''Check if there's black in a given pixel range'''

        # Bei Seiten den um radius entfernten Block testen

        side_blocks = [
            (x,         y),
            (x-radius,  y),
            (x+radius,  y),
            (x,         y-radius),
            (x,         y+radius),
        ]

        for block in side_blocks:
            if self.get_block_at(*block) in self.UNTOUCHABLE_COLORS:
                return True

        # Bei Diagonalen Entfernung zu Ecken berechnen

        corner_blocks = self.get_corner_blocks(x, y)

        for block in corner_blocks:
            if block[1] in self.UNTOUCHABLE_COLORS and coord_distance(x, y, *block[0]) < radius:
                return True

        return False

# Colors

b       = (  0,   0,   0)
w       = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)

# Maps

DEFAULT_MAP = Map(width=800, height=400, spawnpoint=(115, 230) , mymap=[
    (w,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,),
    (w,b,w,w,w,w,w,w,w,w,w,w,w,b,b,b,),
    (w,w,w,w,b,w,w,b,b,w,w,w,w,w,b,b,),
    (b,w,w,w,b,w,w,w,b,b,w,b,w,w,b,b,),
    (b,w,w,w,b,w,b,w,w,w,w,b,w,w,w,b,),
    (b,w,w,w,w,w,w,w,w,w,w,b,b,w,w,b,),
    (b,b,w,w,b,b,b,w,w,w,w,w,w,w,w,b,),
    (b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,b,),
])
