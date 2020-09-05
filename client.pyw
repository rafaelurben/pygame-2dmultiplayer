# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import pygame
from pygame_textinput import TextInput

from client_network import Connection
from player import Player
from maps import Map

DEFAULT_PORT = 9898

server = "localhost"
port = DEFAULT_PORT
playername = None

pygame.display.set_caption("Client")
pygame.base.init()

win = pygame.display.set_mode((400, 100))
font = pygame.font.SysFont('Arial', 12)
clock = pygame.time.Clock()


def redrawWindow(win, players, mymap):
    win.fill((255,255,255))
    mymap.draw(win)
    for player in players:
        player.draw(win, font)
    pygame.display.update()

def showNameChange():
    global win, playername

    pygame.display.set_caption("Client - Name festlegen")
    win = pygame.display.set_mode((400, 100))

    textinput = TextInput(initial_string=playername or "")

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
            playername = textinput.get_text()
            pygame.display.set_caption("Name wurde geändert!")
            return

        # Blit its surface onto the screen
        win.blit(font.render("Spielername: ", True, (0,0,0)), (10,10))
        win.blit(textinput.get_surface(), (10, 30))

        pygame.display.update()
        clock.tick(30)

def showStartScreen():
    global win, server, port

    pygame.display.set_caption("Client")
    win = pygame.display.set_mode((400, 100))

    textinput = TextInput(initial_string=server+(":"+str(port) if port != DEFAULT_PORT else ""))

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
            text = textinput.get_text()

            if ":" in text:
                server = text.split(":")[0]
                try:
                    port = int(text.split(":")[1])
                except ValueError:
                    print("Als Port wurde keine Zahl angegeben!")
            else:
                server = text

            pygame.display.set_caption("Client - Verbinden...")
            return

        # Blit its surface onto the screen
        win.blit(font.render("Server IP: ", True, (0,0,0)), (10,10))
        win.blit(textinput.get_surface(), (10, 30))

        if playername:
            win.blit(font.render(f"Spielername: { playername }", True, (0,0,0)), (10,60))

        pygame.display.update()
        clock.tick(30)

def main():
    global win

    try:
        conn = Connection(server=server, port=port, playername=playername)

        player = conn.player
        pygame.display.set_caption("Client - "+player.name)

        mymap = conn.map
        win = pygame.display.set_mode((mymap.width, mymap.height))

    except (AttributeError, TypeError):
        print("Verbindung konnte nicht hergestellt werden!")
        return

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                print("Fenster wurde geschlossen!")
                pygame.base.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.constants.K_ESCAPE]:
            print("Spiel durch ESC verlassen!")
            return

        players = conn.send_receive(player.get_update_data(keys))

        if players is None:
            print("Verbindung zum Server verloren!")
            return

        redrawWindow(win, players, mymap)

showNameChange()
while True:  
    showStartScreen()       
    main()