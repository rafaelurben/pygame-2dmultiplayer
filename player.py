# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame
from time import sleep
from random import randint

from coordinates import calculate_relative_pos, is_out_of_map

class Player():
    def __init__(self, id, x=None, y=None, radius=None, color=None):
        self.id = id
        self.name = "Spieler "+str(id)

        self.radius = radius or 20
        self.angle = 0

        self.x = x or randint(50,250)
        self.y = y or randint(50,250)


        self.color = color or (randint(0,255), randint(0,255), randint(0,255))
        self.velocity = 3

        self.hidden = False

    @property
    def coords(self):
        return (int(self.x), int(self.y))

    @property
    def color_inverted(self):
        return (255-self.color[0],255-self.color[1],255-self.color[2])

    def calculate_relative_pos(self, relative_angle=0, distance=None):
        '''Client: Calculates a relative position'''

        angle = (self.angle + relative_angle) % 360 
        distance = distance or self.radius 

        return calculate_relative_pos(self.x, self.y, angle, distance)

    def out_of_map(self, mymap, x, y):
        return is_out_of_map(x, y, mymap.width, mymap.height, self.radius)

    def draw(self, win, font=None):
        '''Client: Draws the player'''

        if not self.hidden:
            pygame.draw.circle(win, self.color, self.coords, self.radius)

            triangle = (self.calculate_relative_pos(0, self.radius-2), self.calculate_relative_pos(120, self.radius-2), self.calculate_relative_pos(240, self.radius-2))
            pygame.draw.polygon(win, self.color_inverted, triangle)

            pygame.draw.line(win, self.color, self.coords, self.calculate_relative_pos(0, 2*self.radius))

            if font:
                win.blit(font.render(self.name, True, (0,0,0)), (self.x + self.radius + 5, self.y + self.radius + 5))

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

        self.color = (200,200,200)
        sleep(delay)
        self.hidden = True

    def process(self, mymap, data):
        '''Server: Process the changes uploaded by the player'''

        if data["move_left"]:
            self.angle = (self.angle - 2) % 360

        if data["move_right"]:
            self.angle = (self.angle + 2) % 360

        if data["move_up"] and not self.out_of_map(mymap, *self.calculate_relative_pos(0, int(self.velocity))):
            self.x, self.y = self.calculate_relative_pos(0, int(self.velocity))

        if data["move_down"] and not self.out_of_map(mymap, *self.calculate_relative_pos(0, -int(self.velocity/2))):
            self.x, self.y = self.calculate_relative_pos(0, -int(self.velocity/2))

