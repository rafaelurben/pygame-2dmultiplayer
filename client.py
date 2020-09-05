# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame

from network import Network
from player import Player

server = "localhost"
port = 5555

width = 500
height = 500
win = pygame.display.set_mode((width, height))
# win = pygame.display.set_mode((width, height), pygame.constants.RESIZABLE)

pygame.display.set_caption("Client")
pygame.base.init()

font = pygame.font.SysFont('Arial', 12)


def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw(win, font)
    pygame.display.update()


def main():
    global win

    run = True
    network = Network(server=server, port=port)
    player = network.player
    clock = pygame.time.Clock()

    pygame.display.set_caption("Client - "+player.name)

    while run:
        clock.tick(60)
        players = network.send(player)

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                run = False
                pygame.base.quit()
            # elif event.type == pygame.constants.VIDEORESIZE:
            #     win = pygame.display.set_mode((event.w, event.h), pygame.constants.RESIZABLE)

        try:
            player.movement(win)
            redrawWindow(win, players)
        except pygame.base.error:
            print("Das Fenster wurde geschlossen.")
            break

main()