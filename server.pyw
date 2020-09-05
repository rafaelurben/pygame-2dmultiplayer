# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle
import pygame
from _thread import start_new_thread, interrupt_main
from random import randint
from time import sleep

from player import Player
from maps import Map, DEFAULT_MAP
from pygame_tables import Table

server = "0.0.0.0"
port = 9898

mymap = DEFAULT_MAP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen(5)
print("Server gestartet, warte auf Verbindungen...")

def threaded_interface():
    pygame.base.init()

    win = pygame.display.set_mode((525, 500), pygame.constants.RESIZABLE)
    clock = pygame.time.Clock()

    pygame.display.set_caption(f"Server - Players ({ server }:{ port })")

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
            elif event.type == pygame.constants.VIDEORESIZE:
                win = pygame.display.set_mode((event.w, event.h), pygame.constants.RESIZABLE)

        # Feed it with events every frame

        # if commandinput.update(events):
        #     command = commandinput.get_text()

        # Blit its surface onto the screen

        # win.blit(commandinput.get_surface(), (10, 30))
        
        data = []

        for player in Player.players:
            if not player.hidden:
                data.append(
                    (
                        player.id, 
                        player.name, 
                        player.addr[0],
                        player.addr[1],
                        player.x, 
                        player.y,
                        player.angle,
                    )
                )

        table_settings = [
            ("ID",       3, True),
            ("Name",    20, False),
            ("IP",      15, True),
            ("Port",     6, True),
            ("Coord X",  8, True),
            ("Coord Y",  8, True),
            ("Angle",    5, True),
        ]

        table = Table(data, table_settings)
        table.draw(win)

        pygame.display.update()
        clock.tick(60)

def threaded_client(conn, addr, playerid):
    print(f"Neue Verbindung: { addr } (Spieler { playerid })")

    x, y = mymap.random_spawn()
    player = Player(id=playerid, addr=addr, x=x, y=y)

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
            print("Error:",e)
            break

    print(f"{ player.name } hat die Verbindung verloren.")

    conn.close()
    player.hide()

def main():
    start_new_thread(threaded_interface, tuple())

    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        start_new_thread(threaded_client, (conn, addr, currentPlayer))

        currentPlayer += 1

if __name__ == "__main__":
    main()