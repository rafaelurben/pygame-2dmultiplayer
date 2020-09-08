# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: https://github.com/rafaelurben

# Imports

import pygame

# Relative imports

from modules.pygame_textinput import TextInput
from modules.client_network import Connection
from modules.player import Player
from modules.maps import Map

# Variables

DEFAULT_PORT = 9898

server = "localhost"
port = DEFAULT_PORT
playername = None

# Functions

def redrawWindow(win, players, mymap):
    win.fill((255,255,255))
    mymap.draw(win)
    for player in players:
        player.draw(win, font)
    pygame.display.update()

def showNameChange():
    print("[Client] - Please enter your name...")

    global win, playername

    pygame.display.set_caption("Client [Setup]")
    win = pygame.display.set_mode((400, 100))

    textinput = TextInput(initial_string=playername or "")

    while True:
        win.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.constants.QUIT:
                print("[Client] - Window closed! Exiting...")
                pygame.base.quit()
                exit()

        # Feed it with events every frame
        if textinput.update(events):
            newname = textinput.get_text().strip()
            if newname:
                playername = newname
                print(f"[Client] - Name was set to '{ newname }'.")
            else:
                print("[Client] - No name specified.")
            return

        # Blit its surface onto the screen
        win.blit(font.render("Name: ", True, (0,0,0)), (10,10))
        win.blit(textinput.get_surface(), (10, 30))

        pygame.display.update()
        clock.tick(30)

def showStartScreen():
    print("[Client] - Please enter server IP address (and port)...")

    global win, server, port

    pygame.display.set_caption("Client"+(" - "+playername if playername else "")+" [Menu]")
    win = pygame.display.set_mode((400, 100))

    textinput = TextInput(initial_string=server+(":"+str(port) if port != DEFAULT_PORT else ""))

    while True:
        win.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.constants.QUIT:
                print("[Client] - Window closed! Exiting...")
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
                    print("[Client] - The port isn't a number! Ignoring it.")
            else:
                server = text
            
            print(f"[Client] - Server set to '{ server }:{ port }'!")
            return

        # Blit its surface onto the screen
        win.blit(font.render("Server IP: ", True, (0,0,0)), (10,10))
        win.blit(textinput.get_surface(), (10, 30))

        if playername:
            win.blit(font.render(f"Name: { playername }", True, (0,0,0)), (10,60))

        pygame.display.update()
        clock.tick(30)

def showGame():
    global win

    try:
        pygame.display.set_caption("Client"+(" - "+playername if playername else "")+" [Connecting...]")

        conn = Connection(server=server, port=port, playername=playername)

        if conn.player is None or conn.map is None:
            return

        player = conn.player
        pygame.display.set_caption("Client - "+player.name+" [Game]")

        mymap = conn.map
        win = pygame.display.set_mode((mymap.width, mymap.height))

    except Exception as e:
        print("[Client] - An error occured! Error:",e)
        return

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                print("[Client] - Window closed! Exiting...")
                pygame.base.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.constants.K_ESCAPE]:
            print("[Client] - Pressed ESC! Left game!")
            return

        players = conn.send_receive(player.get_update_data(keys))

        if players is None:
            print("[Client] - Connection lost!")
            return

        redrawWindow(win, players, mymap)

# Init

if __name__ == "__main__":
    pygame.display.set_caption("Client [Initialize...]")
    pygame.base.init()

    win = pygame.display.set_mode((400, 100))
    font = pygame.font.SysFont('Arial', 12)
    clock = pygame.time.Clock()

    print("\n\n")

    showNameChange()
    while True:  
        showStartScreen()       
        showGame()
