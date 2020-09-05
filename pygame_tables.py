# Creator: rafaelurben

import pygame

pygame.font.init()

def to_width(string, length, right=False):
    '''Modify a string to match the given length'''
    string = str(string)
    if len(string) > length:
        return string[:length-2]+".."
    else:
        if right:
            return string.rjust(length)
        else:
            return string.ljust(length)

class Table:
    '''Create a table in pygame'''

    def __init__(self, rows, settings, fontsize=12):
        '''Example:

        rows = [
            ("Rafael", 16, "Switzerland"),
            ("Someone", 100, "Germany")
        ]

        settings = [
            ("Name", 20, False),
            ("Age", 3, True),
            ("Country", 15, False),
            # (Title, Max length, align (right: True, left: False))
        ]
        '''
        self.rows = rows
        self.fontsize = fontsize
        self.settings = settings
        self.font = pygame.font.SysFont('Courier', fontsize)

    def draw(self, win, x=10, y=10):
        win.blit(self.font.render(" ".join(to_width(s[0], s[1], s[2]) for s in self.settings), True, (0,0,0)), (x, y))
        y += self.fontsize+3

        for row in self.rows:
            win.blit(self.font.render(" ".join(to_width(row[i], s[1], s[2]) for i, s in enumerate(self.settings)), True, (0,0,0)), (x, y))
            y += self.fontsize+3
