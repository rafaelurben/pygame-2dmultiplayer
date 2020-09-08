# Original: https://www.youtube.com/channel/UC4JX40jDee_tINbkjycV4Sg
# Edited: https://github.com/rafaelurben

# Imports

import socket
import pickle

# Classes

class Connection:
    def __init__(self, server="localhost", port=5555, playername=None):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.server = server
        self.port = port

        self.addr = (self.server, self.port)

        self.player = None
        self.map = None

        self.__connect(playername)

    def __connect(self, playername=None):
        print(f"[Connection] - Connecting to '{ self.server }:{ self.port }'...")
        try:
            self.__s.connect(self.addr)

            self.player, self.map = self._receive()
            self.player.name = playername if playername else self.player.name

            self._send(self.player.name)

            print(f"[Connection] - Connected to '{ self.server }:{ self.port }'!")
        except Exception as e:
            print(f"[Connection] - Connection to '{ self.server }:{ self.port }' failed! Error:", e)

    def _receive(self):
        try:
            d = self.__s.recv(8192)
            return pickle.loads(d)
        except (pickle.UnpicklingError, EOFError) as e:
            print("[Connection] - UnpicklingError Error:", e) #, "\nData:", d)
            return None

    def _send(self, data):
        try:
            self.__s.send(pickle.dumps(data))
        except (pickle.PicklingError, EOFError) as e:
            print("[Connection] - PicklingError Error:", e) #, "\nData:", data)

    def send_receive(self, data):
        try:
            self._send(data)
            return self._receive() or []
        except socket.error as e:
            print("[Connection] - Error:",e)
            return None
            
