# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: https://github.com/rafaelurben

# Imports

import socket
import pickle

# Classes

class Connection:
    def __init__(self, server="localhost", port=5555, playername=None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server = server
        self.port = port

        self.addr = (self.server, self.port)

        self.player = None
        self.map = None

        self.connect(playername)

    def connect(self, playername=None):
        try:
            self.client.connect(self.addr)
            print(f"Verbunden zu '{ self.server }'!")
            
            self.player, self.map = pickle.loads(self.client.recv(2048))    
            self.player.name = playername if playername else self.player.name
            self.client.send(pickle.dumps(self.player.name))
        except:
            print(f"Verbindung zu '{ self.server }' fehlgeschlagen!")

    def send_receive(self, data):
        try:
            self.client.send(pickle.dumps(data))

            d = self.client.recv(2048)
            try:
                d = pickle.loads(d)
                return d
            except EOFError as e:
                print("Pickle Error:",e,"\nReceived data:",d)
                return []
        except socket.error as e:
            print("Fehler:",e)
            return None
            