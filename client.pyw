# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame
from pygame_textinput import TextInput

from network import ClientNetwork
from player import Player

server = "localhost"
port = 9898

width = 500
height = 500
win = pygame.display.set_mode((width, height))
# win = pygame.display.set_mode((width, height), pygame.constants.RESIZABLE)

pygame.display.set_caption("Client")
pygame.base.init()

font = pygame.font.SysFont('Arial', 12)
clock = pygame.time.Clock()


def redrawWindow(win, players):
    win.fill((255,255,255))
    for player in players:
        player.draw(win, font)
    pygame.display.update()


def showStartScreen():
    global server

    pygame.display.set_caption("Client")

    textinput = TextInput(initial_string=server)

    while True:
        win.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.constants.QUIT:
                print("Das Fenster wurde geschlossen.")
                pygame.base.quit()
                exit()

        # Feed it with events every frame
        if textinput.update(events):
            server = textinput.get_text()
            pygame.display.set_caption("Client - Verbinden...")
            return

        # Blit its surface onto the screen
        win.blit(font.render("Server IP: ", True, (0,0,0)), (10,10))
        win.blit(textinput.get_surface(), (10, 30))

        pygame.display.update()
        clock.tick(30)

def main():
    showStartScreen()

    network = ClientNetwork(server=server, port=port)

    try:
        player = network.player
        pygame.display.set_caption("Client - "+player.name)

    except AttributeError:
        print("Verbindung konnte nicht hergestellt werden!")
        return

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                print("Fenster wurde geschlossen!")
                pygame.base.quit()
                exit()
            # elif event.type == pygame.constants.VIDEORESIZE:
            #     global win
            #     win = pygame.display.set_mode((event.w, event.h), pygame.constants.RESIZABLE)

        keys = pygame.key.get_pressed()

        if keys[pygame.constants.K_ESCAPE]:
            print("Spiel durch ESC verlassen!")
            return

        players = player.update(win, keys, network)

        if not players:
            print("Verbindung zum Server verloren!")
            return

        redrawWindow(win, players)

while True:          
    main()