# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: https://github.com/rafaelurben

# Imports

import socket
import pickle
import pygame
import os.path
from _thread import start_new_thread, interrupt_main
from random import randint
from time import sleep
from argparse import ArgumentParser

# Relative Imports

from modules.player import Player
from modules.maps import Map, DEFAULT_MAP
from modules.pygame_tables import Table

# Variables

server = "0.0.0.0"
port = 9898

mymap = DEFAULT_MAP

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Interface (threaded)

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

# Client connection (threaded)

def threaded_client(conn, addr, playerid):
    print(f"Neue Verbindung: { addr } - #{ playerid }")

    x, y = mymap.random_spawn()
    player = Player(id=playerid, addr=addr, x=x, y=y)

    try:
        data = pickle.dumps((player, mymap))
        conn.send(data)

        player.name = pickle.loads(conn.recv(2048))

        print(f"Spieler { playerid } heisst '{ player.name }'.")

        while True:
            try:
                data = pickle.loads(conn.recv(2048))

                if not data:
                    print(f"Keine Daten von { player.name } erhalten!")
                    break
                else:
                    player.process(mymap, data)

                conn.send(pickle.dumps(Player.players))
            except EOFError:
                print(f"{ player.name } hat die Verbindung verloren.")
                break
            except Exception as e:
                print(f"Die Verbindung von { player.name } wurde unterbrochen. Error:",e)
                break
    except (ConnectionAbortedError, ConnectionResetError):
        print(f"Die Verbindung von { player.name } wurde verweigert oder zurückgesetzt.")

    conn.close()
    player.hide()

# Server loop

def serverLoop():
    currentPlayer = 0
    while True:
        conn, addr = s.accept()
        start_new_thread(threaded_client, (conn, addr, currentPlayer))

        currentPlayer += 1

# Main

def is_valid_file(parser, arg):
    if (not os.path.exists(arg)) or (not os.path.isfile(arg)):
        parser.error("The file %s does not exist!" % arg)
    else:
        return os.path.abspath(arg)

def main():
    global port, mymap

    parser = ArgumentParser(description="Starte den Server")
    parser.add_argument("-p", "--port", type=int, help="The port to be used", default=port)
    parser.add_argument("--nogui", help="Hide the GUI interface", default=False, action='store_true')
    parser.add_argument("-m", "--map", type=lambda arg: is_valid_file(parser, arg), dest="map_path")

    args = parser.parse_args()

    port = args.port
    if not args.nogui:
        start_new_thread(threaded_interface, tuple())
    if args.map_path:
        mymap = Map.from_file(args.map_path)

    try:
        try:
            s.bind((server, port))
        except socket.error as e:
            print(str(e))

        s.listen(5)
        print("Server gestartet, warte auf Verbindungen...")

        serverLoop()
    except KeyboardInterrupt:
        quit()

if __name__ == "__main__":
    print("\n\n")
    main()
