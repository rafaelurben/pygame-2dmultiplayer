# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle

class ClientNetwork:
    def __init__(self, server="localhost", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.player, self.map = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            print(f"Verbunden zu '{ self.server }'!")
            return pickle.loads(self.client.recv(2048))
        except:
            print(f"Verbindung zu '{ self.server }' fehlgeschlagen!")
            return None

    def send_receive(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Fehler:",e)
            return None
            