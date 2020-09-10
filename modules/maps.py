# Creator: https://github.com/rafaelurben

# Imports

import pygame
import numpy
from PIL import Image
from random import randint

# Relative Imports

from .coordinates import ceil, floor, sin, coord_distance

# Classes

class Map:
    def __init__(self, width, height, mymap=[], spawnpoint=None, spawn_range=5):
        self.width = width
        self.height = height
        self.map = mymap

        self.spawnpoint = spawnpoint or (width/2, height/2)
        self.spawn_range = spawn_range

        self.blocks_horizontal = len(self.map[0]) if self.map else 0
        self.blocks_vertical = len(self.map)
        self.block_width = self.width/self.blocks_horizontal if self.blocks_horizontal else self.width
        self.block_height = self.height/self.blocks_vertical if self.blocks_vertical else self.height

        self.UNTOUCHABLE_COLORS = [(0, 0, 0), (1, 1, 1)]

    def random_spawn(self):
        '''Get a random spawnpoint'''
        
        return (randint(int(self.spawnpoint[0]-self.spawn_range), int(self.spawnpoint[0]+self.spawn_range)), randint(int(self.spawnpoint[1]-self.spawn_range), int(self.spawnpoint[1]+self.spawn_range)))

    def draw(self, win):
        '''Draw the map on a pygame surface'''

        for r, row in enumerate(self.map):
            for c, color in enumerate(row):
                rect = ((c*self.block_width,r*self.block_height),((c+1)*self.block_width,(r+1)*self.block_height))
                pygame.draw.rect(win, color, rect)

    # Utility functions

    def get_block_at(self, x, y):
        '''Get the block color at specified coordinates'''

        if self.map == [] or x > self.width or y > self.height:
            return (255, 255, 255)
        else: 
            return tuple(self.map[int(y/self.block_height)][int(x/self.block_width)])    

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


    def can_go_to(self, x, y, radius):
        '''Check if there's black in a given pixel range'''

        # Map border

        if x-radius < 0 or y-radius < 0 or x+radius > self.width or y+radius > self.height:
            return False

        # Wenn keine Karte vorhanden, darf alles berührt werden

        if self.map == []:
            return True

        # Bei Seiten den um radius entfernten Block testen

        side_blocks = [
            (x,         y),
            (x-radius,  y),
            (x+radius,  y),
            (x,         y-radius),
            (x,         y+radius),
        ]

        for block in side_blocks:
            color = self.get_block_at(*block)
            if color in self.UNTOUCHABLE_COLORS:
                return False

        # Bei Diagonalen Entfernung zu Ecken berechnen

        corner_blocks = self.get_corner_blocks(x, y)

        for block in corner_blocks:
            if block[1] in self.UNTOUCHABLE_COLORS and coord_distance(x, y, *block[0]) < radius:
                return False

        return True

    # Classmethods

    @classmethod
    def from_file(self, filepath):
        '''Create map from image file'''

        img = Image.open(filepath)
        if not img.mode == "RGB":
            img = img.convert('RGB')

        img_sequence = img.getdata()
        img_array = numpy.array(img_sequence)

        array = [
            img_array[i*img.width:(i+1)*img.width].tolist() for i in range(img.height)
        ]

        width = img.width
        height = img.height

        while width<800 and height<400:
            width *= 2
            height *= 2

        return Map(width=width, height=height, mymap=array)


# Colors

b       = (  0,   0,   0)
w       = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)

