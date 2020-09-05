# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame
from time import sleep

class Player():
    def __init__(self, id, x, y, width, height, color):
        self.id = id
        self.name = "Spieler "+str(id)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velocity = 3

        self.hidden = False

    @property
    def rect(self):
        return (self.x, self.y, self.width, self.height)

    def hide(self):
        self.color = (200,200,200)
        sleep(3)
        self.hidden = True

    def draw(self, win, font=None):
        if not self.hidden:
            pygame.draw.rect(win, self.color, self.rect)
            if font:
                win.blit(font.render(self.name, True, (0,0,0)), (self.x + self.width + 5, self.y + self.height + 5))

    def get_update_data(self, keys):
        '''Client: Upload changes and download players'''

        data = {
            "move_left":    (keys[pygame.constants.K_LEFT]  or keys[pygame.constants.K_a]),
            "move_right":   (keys[pygame.constants.K_RIGHT] or keys[pygame.constants.K_d]),
            "move_up":      (keys[pygame.constants.K_UP]    or keys[pygame.constants.K_w]),
            "move_down":    (keys[pygame.constants.K_DOWN]  or keys[pygame.constants.K_s]),
        }

        return data

    def process(self, mymap, data):
        '''Server: Process the changes uploaded by the player'''

        win_width = mymap.width
        win_height = mymap.height

        if data["move_left"]    and self.x >= self.velocity:
            self.x -= self.velocity

        if data["move_right"]   and self.x + self.velocity + self.width <= win_width:
            self.x += self.velocity

        if data["move_up"]      and self.y >= self.velocity:
            self.y -= self.velocity

        if data["move_down"]    and self.y + self.velocity + self.height <= win_height:
            self.y += self.velocity

