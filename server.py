# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle
from _thread import start_new_thread
from random import randint
from time import sleep

from player import Player

server = "0.0.0.0"
port = 9898

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(5)
print("Server gestartet, warte auf Verbindungen...")


players = []

def create_random_player(playerid):
    player = Player(id=playerid, x=randint(50,250), y=randint(50,250), width=50, height=50, color=(randint(0,255),randint(0,255),randint(0,255)))
    players.append(player)
    return player

def threaded_client(conn, player):
    conn.send(pickle.dumps(player))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if not data:
                print("Verbindung zu Spieler", player.id, "getrennt")
                break
            else:
                player.process(data)

            conn.send(pickle.dumps(players))
        except:
            break

    print("Spieler",player.id,"hat die Verbindung verloren.")

    conn.close()
    player.hide()

currentPlayer = 0
while True:
    conn, addr = s.accept()

    print("Neue Verbindung:",addr, f"(Spieler {str(currentPlayer)})")

    player = create_random_player(currentPlayer)

    thread = start_new_thread(threaded_client, (conn, player))

    currentPlayer += 1
