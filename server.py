# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle
from _thread import start_new_thread
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


players = []

def create_random_player(playerid):
    player = Player(id=playerid)
    players.append(player)
    return player

def threaded_client(conn, addr, playerid):
    print(f"Neue Verbindung: { addr } (Spieler { playerid })")

    player = create_random_player(playerid)

    conn.send(pickle.dumps((player, mymap)))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print(f"Verbindung zu { player.name } getrennt")
                break
            else:
                player.process(mymap, data)

            conn.send(pickle.dumps(players))
        except:
            break

    print(f"{ player.name } hat die Verbindung verloren.")

    conn.close()
    player.hide()
    players.remove(player)

currentPlayer = 0
while True:
    conn, addr = s.accept()
    thread = start_new_thread(threaded_client, (conn, addr, currentPlayer))

    currentPlayer += 1
