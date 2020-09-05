# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: rafaelurben

import socket
import pickle

class Network:
    def __init__(self, server="localhost", port=5555):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (self.server, self.port)
        self.player = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Verbunden!")
            return pickle.loads(self.client.recv(2048))
        except:
            print("Verbindung fehlgeschlagen!")

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print("Fehler:",e)