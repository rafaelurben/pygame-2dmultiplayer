# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame
from time import sleep
from random import randint

from coordinates import calculate_relative_pos, is_out_of_map, coord_distance, coord_angle

class Player():
    players = []

    def __init__(self, id, x=None, y=None, radius=None, color=None, addr=None):
        self.id = id
        self.name = "Spieler "+str(id)

        self.radius = radius or 15
        self.angle = 270

        self.x = x or randint(50,250)
        self.y = y or randint(50,250)


        self.color = color or (randint(0,255), randint(0,255), randint(0,255))
        self.velocity = 3

        self.hidden = False

        self.addr = addr

        self.players.append(self)

    @property
    def coords(self):
        '''Client: Get current coords'''

        return (int(self.x), int(self.y))

    @property
    def color_inverted(self):
        '''Client: Get the inverted color'''

        return (255-self.color[0],255-self.color[1],255-self.color[2])

    def calculate_relative_pos(self, relative_angle=0, distance=None):
        '''Client: Calculates a relative position'''

        angle = (self.angle + relative_angle) % 360 
        distance = distance or self.radius 

        return calculate_relative_pos(self.x, self.y, angle, distance)

    def out_of_map(self, mymap, x, y):
        '''Client: Check if a coordinate is out of map'''

        return is_out_of_map(x, y, mymap.width, mymap.height, self.radius)

    def draw(self, win, font=None):
        '''Client: Draws the player'''

        pygame.draw.circle(win, self.color, self.coords, self.radius)

        triangle = (self.calculate_relative_pos(0, self.radius-2), self.calculate_relative_pos(120, self.radius-2), self.calculate_relative_pos(240, self.radius-2))
        pygame.draw.polygon(win, self.color_inverted, triangle)

        pygame.draw.line(win, self.color, self.coords, self.calculate_relative_pos(0, 2*self.radius))

        if font:
            win.blit(font.render(self.name, True, (50,50,50)), (self.x + self.radius + 5, self.y + self.radius + 5))

    def get_update_data(self, keys):
        '''Client: Upload changes and download players'''

        data = {
            "move_left":    (keys[pygame.constants.K_LEFT]  or keys[pygame.constants.K_a]),
            "move_right":   (keys[pygame.constants.K_RIGHT] or keys[pygame.constants.K_d]),
            "move_up":      (keys[pygame.constants.K_UP]    or keys[pygame.constants.K_w]),
            "move_down":    (keys[pygame.constants.K_DOWN]  or keys[pygame.constants.K_s]),
        }

        return data

    def hide(self, delay=3):
        '''Server: Makes the player gray and makes him disappear after delay'''

        self.hidden = True
        self.color = (200,200,200)
        
        sleep(delay)

        self.players.remove(self)

    def process(self, mymap, data):
        '''Server: Process the changes uploaded by the player'''

        x, y = self.x, self.y

        if data["move_left"]:
            self.angle = (self.angle - 2) % 360

        if data["move_right"]:
            self.angle = (self.angle + 2) % 360

        if data["move_up"] and not data["move_down"]:
            newpos = self.calculate_relative_pos(0, int(self.velocity))
            if not self.out_of_map(mymap, *newpos):
                x, y = newpos
        if data["move_down"] and not data["move_up"]:
            newpos = self.calculate_relative_pos(0, -int(self.velocity/2))
            if not self.out_of_map(mymap, *newpos):
                x, y = newpos

        if (x != self.x or y != self.y) and self.can_move_to(x, y, mymap):
            self.x, self.y = x, y

    def can_move_to(self, x, y, mymap):
        '''Server: Checks if player would touch the map or another player'''

        # Check for map 

        block = mymap.get_block_at(x, y)
        if block == (0, 0, 0):
            return False
        
        # Check for players

        players = list(self.players)
        players.remove(self)

        for player in players:
            if not player.hidden:
                distance = coord_distance(x, y, *player.coords)
                if distance < self.radius + player.radius:
                    return False
        return True

        