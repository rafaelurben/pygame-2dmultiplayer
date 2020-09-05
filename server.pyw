# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle
import pygame
from _thread import start_new_thread, interrupt_main
from random import randint
from time import sleep

from player import Player
from maps import Map

server = "0.0.0.0"
port = 9898
mymap = Map(width=800, height=400)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Server gestartet, warte auf Verbindungen...")

def threaded_interface():
    pygame.base.init()

    win = pygame.display.set_mode((500, 500))
    font = pygame.font.SysFont('Arial', 12)
    clock = pygame.time.Clock()

    pygame.display.set_caption("Server - Players")

    # commandinput = TextInput()

    while True:
        win.fill((225, 225, 225))

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.constants.QUIT:
                print("Das Fenster wurde geschlossen. Server wird beendet...")
                pygame.base.quit()
                interrupt_main()
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("localhost", port))
                exit()

        # Feed it with events every frame

        # if commandinput.update(events):
        #     command = commandinput.get_text()

        # Blit its surface onto the screen

        # win.blit(commandinput.get_surface(), (10, 30))

        y = 10

        for player in Player.players:
            if not player.hidden:
                win.blit(font.render(f"{ str(player.id).zfill(2) }: { player.name }", True, (0,0,0)), (10,y))
                y += 15

        pygame.display.update()
        clock.tick(60)

def threaded_client(conn, addr, playerid):
    print(f"Neue Verbindung: { addr } (Spieler { playerid })")

    player = Player(id=playerid)

    conn.send(pickle.dumps((player, mymap)))
    player.name = pickle.loads(conn.recv(2048))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print(f"Verbindung zu { player.name } getrennt!")
                break
            else:
                player.process(mymap, data)

            conn.send(pickle.dumps(Player.players))
        except Exception as e:
            print("Fatal exception:",e)
            break

    print(f"{ player.name } hat die Verbindung verloren.")

    conn.close()
    player.hide()

start_new_thread(threaded_interface, tuple())

currentPlayer = 0
while True:
    conn, addr = s.accept()
    thread = start_new_thread(threaded_client, (conn, addr, currentPlayer))

    currentPlayer += 1
